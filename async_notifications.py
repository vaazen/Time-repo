"""
🔔 Асинхронная система умных уведомлений
Обеспечивает эффективную доставку уведомлений с адаптивными алгоритмами
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import queue
from pathlib import Path
import uuid

from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QThread
from PyQt5.QtWidgets import QSystemTrayIcon, QMessageBox, QApplication
from PyQt5.QtGui import QIcon

from config_manager import get_config
from cache_manager import cached, get_cache_manager

class NotificationType(Enum):
    """Типы уведомлений"""
    TASK_REMINDER = "task_reminder"
    BREAK_SUGGESTION = "break_suggestion"
    PRODUCTIVITY_ALERT = "productivity_alert"
    DEADLINE_WARNING = "deadline_warning"
    FOCUS_TIME = "focus_time"
    ACHIEVEMENT = "achievement"
    SYSTEM_INFO = "system_info"
    ERROR = "error"

class NotificationPriority(Enum):
    """Приоритеты уведомлений"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

class NotificationChannel(Enum):
    """Каналы доставки уведомлений"""
    SYSTEM_TRAY = "system_tray"
    POPUP = "popup"
    SLACK = "slack"
    EMAIL = "email"
    SOUND = "sound"
    DESKTOP = "desktop"

@dataclass
class Notification:
    """Модель уведомления"""
    id: str
    type: NotificationType
    priority: NotificationPriority
    title: str
    message: str
    channels: List[NotificationChannel]
    scheduled_time: datetime
    created_at: datetime
    task_id: Optional[str] = None
    user_id: Optional[str] = None
    metadata: Dict[str, Any] = None
    retry_count: int = 0
    max_retries: int = 3
    delivered: bool = False
    read: bool = False
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class NotificationRule:
    """Правило для создания уведомлений"""
    
    def __init__(self, name: str, condition: Callable, 
                 notification_factory: Callable, enabled: bool = True):
        self.name = name
        self.condition = condition
        self.notification_factory = notification_factory
        self.enabled = enabled
        self.last_triggered = None

class NotificationDeliveryService:
    """Сервис доставки уведомлений"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.delivery_handlers = {}
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """Регистрация обработчиков по умолчанию"""
        self.delivery_handlers[NotificationChannel.SYSTEM_TRAY] = self._deliver_system_tray
        self.delivery_handlers[NotificationChannel.POPUP] = self._deliver_popup
        self.delivery_handlers[NotificationChannel.DESKTOP] = self._deliver_desktop
        self.delivery_handlers[NotificationChannel.SOUND] = self._deliver_sound
    
    async def deliver(self, notification: Notification) -> bool:
        """Доставка уведомления по всем каналам"""
        success = True
        
        for channel in notification.channels:
            try:
                handler = self.delivery_handlers.get(channel)
                if handler:
                    await handler(notification)
                else:
                    self.logger.warning(f"Нет обработчика для канала {channel}")
                    success = False
            except Exception as e:
                self.logger.error(f"Ошибка доставки через {channel}: {e}")
                success = False
        
        return success
    
    async def _deliver_system_tray(self, notification: Notification):
        """Доставка через системный трей"""
        try:
            app = QApplication.instance()
            if app and hasattr(app, 'tray_icon'):
                app.tray_icon.showMessage(
                    notification.title,
                    notification.message,
                    QSystemTrayIcon.Information,
                    5000  # 5 секунд
                )
        except Exception as e:
            self.logger.error(f"Ошибка системного трея: {e}")
    
    async def _deliver_popup(self, notification: Notification):
        """Доставка через всплывающее окно"""
        try:
            # Запускаем в главном потоке Qt
            def show_popup():
                QMessageBox.information(
                    None,
                    notification.title,
                    notification.message
                )
            
            # Планируем выполнение в главном потоке
            QTimer.singleShot(0, show_popup)
            
        except Exception as e:
            self.logger.error(f"Ошибка popup: {e}")
    
    async def _deliver_desktop(self, notification: Notification):
        """Доставка через desktop notification (Windows/Linux)"""
        try:
            import plyer
            plyer.notification.notify(
                title=notification.title,
                message=notification.message,
                timeout=5
            )
        except ImportError:
            self.logger.warning("plyer не установлен для desktop уведомлений")
        except Exception as e:
            self.logger.error(f"Ошибка desktop уведомления: {e}")
    
    async def _deliver_sound(self, notification: Notification):
        """Доставка звукового уведомления"""
        try:
            import winsound
            if notification.priority == NotificationPriority.URGENT:
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            else:
                winsound.MessageBeep(winsound.MB_ICONINFORMATION)
        except ImportError:
            pass  # winsound доступен только на Windows
        except Exception as e:
            self.logger.error(f"Ошибка звукового уведомления: {e}")

class AsyncNotificationManager(QObject):
    """Асинхронный менеджер уведомлений"""
    
    notification_sent = pyqtSignal(str)  # ID уведомления
    notification_failed = pyqtSignal(str, str)  # ID, ошибка
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.config = get_config()
        
        # Очереди и сервисы
        self.notification_queue = asyncio.Queue()
        self.scheduled_notifications = []
        self.delivery_service = NotificationDeliveryService()
        
        # Правила и статистика
        self.rules = []
        self.notification_history = []
        self.user_preferences = self._load_user_preferences()
        
        # Асинхронный цикл
        self.loop = None
        self.running = False
        
        # Кэш для частых запросов
        self.cache = get_cache_manager()
        
        # Запускаем асинхронный обработчик
        self._start_async_processor()
    
    def _start_async_processor(self):
        """Запуск асинхронного обработчика"""
        def run_async_loop():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.running = True
            
            try:
                self.loop.run_until_complete(self._async_processor())
            except Exception as e:
                self.logger.error(f"Ошибка в асинхронном процессоре: {e}")
            finally:
                self.running = False
        
        thread = threading.Thread(target=run_async_loop, daemon=True)
        thread.start()
    
    async def _async_processor(self):
        """Основной асинхронный обработчик"""
        while self.running:
            try:
                # Обрабатываем очередь уведомлений
                await self._process_notification_queue()
                
                # Проверяем запланированные уведомления
                await self._check_scheduled_notifications()
                
                # Применяем правила
                await self._apply_notification_rules()
                
                # Небольшая пауза
                await asyncio.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Ошибка в обработчике уведомлений: {e}")
                await asyncio.sleep(5)
    
    async def _process_notification_queue(self):
        """Обработка очереди уведомлений"""
        try:
            # Обрабатываем все уведомления в очереди
            while not self.notification_queue.empty():
                notification = await asyncio.wait_for(
                    self.notification_queue.get(), timeout=0.1
                )
                await self._deliver_notification(notification)
                
        except asyncio.TimeoutError:
            pass  # Очередь пуста
        except Exception as e:
            self.logger.error(f"Ошибка обработки очереди: {e}")
    
    async def _deliver_notification(self, notification: Notification):
        """Доставка уведомления"""
        try:
            # Проверяем пользовательские настройки
            if not self._should_deliver(notification):
                return
            
            # Доставляем уведомление
            success = await self.delivery_service.deliver(notification)
            
            if success:
                notification.delivered = True
                self.notification_sent.emit(notification.id)
                self.logger.info(f"Уведомление {notification.id} доставлено")
            else:
                notification.retry_count += 1
                if notification.retry_count < notification.max_retries:
                    # Повторная попытка через некоторое время
                    await asyncio.sleep(2 ** notification.retry_count)
                    await self.notification_queue.put(notification)
                else:
                    self.notification_failed.emit(notification.id, "Превышено количество попыток")
            
            # Сохраняем в историю
            self.notification_history.append(notification)
            
            # Ограничиваем размер истории
            if len(self.notification_history) > 1000:
                self.notification_history = self.notification_history[-500:]
                
        except Exception as e:
            self.logger.error(f"Ошибка доставки уведомления {notification.id}: {e}")
            self.notification_failed.emit(notification.id, str(e))
    
    async def _check_scheduled_notifications(self):
        """Проверка запланированных уведомлений"""
        now = datetime.now()
        ready_notifications = []
        
        for notification in self.scheduled_notifications[:]:
            if notification.scheduled_time <= now:
                ready_notifications.append(notification)
                self.scheduled_notifications.remove(notification)
        
        for notification in ready_notifications:
            await self.notification_queue.put(notification)
    
    async def _apply_notification_rules(self):
        """Применение правил уведомлений"""
        for rule in self.rules:
            if not rule.enabled:
                continue
            
            try:
                if rule.condition():
                    # Проверяем, не срабатывало ли правило недавно
                    if (rule.last_triggered and 
                        datetime.now() - rule.last_triggered < timedelta(minutes=5)):
                        continue
                    
                    notification = rule.notification_factory()
                    if notification:
                        await self.send_notification(notification)
                        rule.last_triggered = datetime.now()
                        
            except Exception as e:
                self.logger.error(f"Ошибка в правиле {rule.name}: {e}")
    
    def _should_deliver(self, notification: Notification) -> bool:
        """Проверка, следует ли доставлять уведомление"""
        # Проверяем настройки пользователя
        if not self.config.ui.show_notifications:
            return False
        
        # Проверяем время "не беспокоить"
        now = datetime.now().time()
        if hasattr(self.user_preferences, 'quiet_hours'):
            start, end = self.user_preferences['quiet_hours']
            if start <= now <= end:
                return notification.priority == NotificationPriority.URGENT
        
        # Проверяем частоту уведомлений
        recent_count = sum(1 for n in self.notification_history[-10:] 
                          if n.type == notification.type)
        if recent_count >= 3:  # Не более 3 уведомлений одного типа подряд
            return notification.priority >= NotificationPriority.HIGH
        
        return True
    
    def _load_user_preferences(self) -> Dict:
        """Загрузка пользовательских настроек"""
        try:
            prefs_file = Path("user_notification_preferences.json")
            if prefs_file.exists():
                with open(prefs_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"Ошибка загрузки настроек: {e}")
        
        return {
            'quiet_hours': None,
            'preferred_channels': [NotificationChannel.SYSTEM_TRAY.value],
            'priority_threshold': NotificationPriority.MEDIUM.value
        }
    
    # Публичные методы
    
    async def send_notification(self, notification: Notification):
        """Отправка уведомления"""
        await self.notification_queue.put(notification)
    
    def send_notification_sync(self, notification: Notification):
        """Синхронная отправка уведомления"""
        if self.loop and self.running:
            asyncio.run_coroutine_threadsafe(
                self.send_notification(notification), self.loop
            )
    
    def schedule_notification(self, notification: Notification):
        """Планирование уведомления"""
        self.scheduled_notifications.append(notification)
        self.scheduled_notifications.sort(key=lambda n: n.scheduled_time)
    
    def add_rule(self, rule: NotificationRule):
        """Добавление правила уведомлений"""
        self.rules.append(rule)
    
    def remove_rule(self, rule_name: str):
        """Удаление правила уведомлений"""
        self.rules = [r for r in self.rules if r.name != rule_name]
    
    @cached(ttl=60)  # Кэшируем на 1 минуту
    def get_statistics(self) -> Dict[str, Any]:
        """Получение статистики уведомлений"""
        total = len(self.notification_history)
        if total == 0:
            return {'total': 0}
        
        delivered = sum(1 for n in self.notification_history if n.delivered)
        by_type = {}
        by_priority = {}
        
        for notification in self.notification_history:
            # По типам
            type_name = notification.type.value
            by_type[type_name] = by_type.get(type_name, 0) + 1
            
            # По приоритетам
            priority_name = notification.priority.name
            by_priority[priority_name] = by_priority.get(priority_name, 0) + 1
        
        return {
            'total': total,
            'delivered': delivered,
            'delivery_rate': (delivered / total) * 100,
            'by_type': by_type,
            'by_priority': by_priority,
            'queue_size': self.notification_queue.qsize(),
            'scheduled_count': len(self.scheduled_notifications)
        }
    
    def stop(self):
        """Остановка менеджера"""
        self.running = False
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)

# Фабричные функции для создания уведомлений

def create_task_reminder(task_id: str, task_title: str, 
                        scheduled_time: datetime) -> Notification:
    """Создание напоминания о задаче"""
    return Notification(
        id=str(uuid.uuid4()),
        type=NotificationType.TASK_REMINDER,
        priority=NotificationPriority.MEDIUM,
        title="Напоминание о задаче",
        message=f"Время выполнить: {task_title}",
        channels=[NotificationChannel.SYSTEM_TRAY, NotificationChannel.SOUND],
        scheduled_time=scheduled_time,
        created_at=datetime.now(),
        task_id=task_id
    )

def create_break_suggestion(work_duration: int) -> Notification:
    """Создание предложения о перерыве"""
    return Notification(
        id=str(uuid.uuid4()),
        type=NotificationType.BREAK_SUGGESTION,
        priority=NotificationPriority.LOW,
        title="Время для перерыва",
        message=f"Вы работаете уже {work_duration} минут. Рекомендуем сделать перерыв.",
        channels=[NotificationChannel.SYSTEM_TRAY],
        scheduled_time=datetime.now(),
        created_at=datetime.now(),
        metadata={'work_duration': work_duration}
    )

def create_deadline_warning(task_title: str, hours_left: int) -> Notification:
    """Создание предупреждения о дедлайне"""
    priority = NotificationPriority.URGENT if hours_left <= 2 else NotificationPriority.HIGH
    
    return Notification(
        id=str(uuid.uuid4()),
        type=NotificationType.DEADLINE_WARNING,
        priority=priority,
        title="Приближается дедлайн!",
        message=f"До завершения '{task_title}' осталось {hours_left} часов",
        channels=[NotificationChannel.SYSTEM_TRAY, NotificationChannel.POPUP, NotificationChannel.SOUND],
        scheduled_time=datetime.now(),
        created_at=datetime.now(),
        metadata={'hours_left': hours_left}
    )

# Глобальный экземпляр менеджера
notification_manager = AsyncNotificationManager()

def get_notification_manager() -> AsyncNotificationManager:
    """Получение глобального менеджера уведомлений"""
    return notification_manager
