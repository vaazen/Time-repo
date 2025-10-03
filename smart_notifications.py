# smart_notifications.py - Умная система уведомлений с адаптивными алгоритмами
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import pickle
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QThread
from PyQt5.QtWidgets import QSystemTrayIcon, QMessageBox, QApplication
from PyQt5.QtGui import QIcon
import requests
import calendar

class NotificationType(Enum):
    TASK_REMINDER = "task_reminder"
    BREAK_SUGGESTION = "break_suggestion"
    PRODUCTIVITY_ALERT = "productivity_alert"
    DEADLINE_WARNING = "deadline_warning"
    FOCUS_TIME = "focus_time"
    ACHIEVEMENT = "achievement"

class NotificationPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

@dataclass
class SmartNotification:
    """Умное уведомление с контекстом"""
    id: str
    type: NotificationType
    priority: NotificationPriority
    title: str
    message: str
    scheduled_time: datetime
    task_id: Optional[str] = None
    user_response: Optional[str] = None
    effectiveness_score: float = 0.0
    context_data: Dict = None

class UserBehaviorAnalyzer:
    """Анализатор поведения пользователя для адаптивных уведомлений"""
    
    def __init__(self, data_file="user_behavior_data.json"):
        self.data_file = data_file
        self.behavior_data = self.load_behavior_data()
        
    def load_behavior_data(self) -> Dict:
        """Загрузка данных о поведении пользователя"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "notification_responses": [],
            "productivity_patterns": {},
            "break_preferences": {},
            "focus_periods": [],
            "task_completion_times": {},
            "optimal_notification_times": {}
        }
    
    def save_behavior_data(self):
        """Сохранение данных о поведении"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.behavior_data, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            print(f"Ошибка сохранения данных поведения: {e}")
    
    def record_notification_response(self, notification_id: str, response: str, 
                                   response_time: float):
        """Записать реакцию пользователя на уведомление"""
        self.behavior_data["notification_responses"].append({
            "notification_id": notification_id,
            "response": response,  # "dismissed", "snoozed", "completed", "ignored"
            "response_time": response_time,
            "timestamp": datetime.now().isoformat()
        })
        self.save_behavior_data()
    
    def analyze_productivity_patterns(self) -> Dict:
        """Анализ паттернов продуктивности по времени дня и дням недели"""
        patterns = {}
        
        # Анализ по часам дня
        hourly_productivity = {}
        for hour in range(24):
            hourly_productivity[hour] = self._calculate_hourly_productivity(hour)
        
        patterns["hourly"] = hourly_productivity
        
        # Анализ по дням недели
        weekly_productivity = {}
        for day in range(7):  # 0 = понедельник
            weekly_productivity[day] = self._calculate_daily_productivity(day)
        
        patterns["weekly"] = weekly_productivity
        
        return patterns
    
    def _calculate_hourly_productivity(self, hour: int) -> float:
        """Расчет продуктивности для конкретного часа"""
        # Здесь будет логика анализа завершенных задач в этот час
        # Пока возвращаем базовое значение
        base_productivity = 0.7
        
        # Утренние часы обычно более продуктивны
        if 9 <= hour <= 11:
            return min(1.0, base_productivity + 0.2)
        elif 14 <= hour <= 16:
            return min(1.0, base_productivity + 0.1)
        elif 20 <= hour <= 23 or 0 <= hour <= 6:
            return max(0.1, base_productivity - 0.3)
        
        return base_productivity
    
    def _calculate_daily_productivity(self, day: int) -> float:
        """Расчет продуктивности для дня недели"""
        # 0 = понедельник, 6 = воскресенье
        weekday_productivity = {
            0: 0.8,  # понедельник
            1: 0.9,  # вторник
            2: 0.85, # среда
            3: 0.8,  # четверг
            4: 0.7,  # пятница
            5: 0.5,  # суббота
            6: 0.4   # воскресенье
        }
        return weekday_productivity.get(day, 0.7)
    
    def get_optimal_notification_time(self, notification_type: NotificationType) -> datetime:
        """Определение оптимального времени для уведомления"""
        now = datetime.now()
        patterns = self.analyze_productivity_patterns()
        
        current_hour = now.hour
        current_day = now.weekday()
        
        # Для напоминаний о задачах - выбираем более продуктивное время
        if notification_type == NotificationType.TASK_REMINDER:
            best_hours = sorted(patterns["hourly"].items(), 
                              key=lambda x: x[1], reverse=True)[:3]
            
            for hour, _ in best_hours:
                if hour > current_hour:
                    return now.replace(hour=hour, minute=0, second=0, microsecond=0)
        
        # Для перерывов - после периодов высокой активности
        elif notification_type == NotificationType.BREAK_SUGGESTION:
            return now + timedelta(minutes=25)  # Техника Помодоро
        
        return now + timedelta(minutes=5)  # По умолчанию

class CalendarIntegration:
    """Интеграция с внешними календарями"""
    
    def __init__(self):
        self.google_calendar_enabled = False
        self.outlook_enabled = False
    
    def sync_with_google_calendar(self, api_key: str = None):
        """Синхронизация с Google Calendar"""
        # Здесь будет реализация Google Calendar API
        try:
            # Пример интеграции (требует настройки API)
            self.google_calendar_enabled = True
            return True
        except Exception as e:
            print(f"Ошибка синхронизации с Google Calendar: {e}")
            return False
    
    def get_upcoming_events(self, hours_ahead: int = 24) -> List[Dict]:
        """Получение предстоящих событий из календарей"""
        events = []
        
        # Здесь будет логика получения событий из внешних календарей
        # Пока возвращаем пример
        now = datetime.now()
        events.append({
            "title": "Встреча с командой",
            "start_time": now + timedelta(hours=2),
            "end_time": now + timedelta(hours=3),
            "source": "google_calendar"
        })
        
        return events

class SmartNotificationManager(QObject):
    """Менеджер умных уведомлений"""
    
    notification_sent = pyqtSignal(str, str, str)  # title, message, type
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.behavior_analyzer = UserBehaviorAnalyzer()
        self.calendar_integration = CalendarIntegration()
        self.notifications_queue = []
        self.active_notifications = {}
        self.check_timer = None
        
        # Отложенная инициализация таймера
        self.init_timer_delayed()
        
        # Системный трей для уведомлений
        self.setup_system_tray()
    
    def init_timer_delayed(self):
        """Отложенная инициализация таймера в правильном потоке"""
        from PyQt5.QtCore import QTimer
        if self.check_timer is None:
            self.check_timer = QTimer(self)
            self.check_timer.timeout.connect(self.check_notifications)
            self.check_timer.start(30000)  # Проверяем каждые 30 секунд
    
    def setup_system_tray(self):
        """Настройка системного трея"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon()
            # Здесь можно добавить иконку
            self.tray_icon.show()
    
    def schedule_smart_notification(self, task_id: str, task_title: str, 
                                  task_start_time: datetime, 
                                  notification_type: NotificationType = NotificationType.TASK_REMINDER):
        """Планирование умного уведомления"""
        
        # Анализируем оптимальное время
        optimal_time = self.behavior_analyzer.get_optimal_notification_time(notification_type)
        
        # Создаем уведомление
        notification = SmartNotification(
            id=f"{task_id}_{notification_type.value}_{datetime.now().timestamp()}",
            type=notification_type,
            priority=self._determine_priority(task_start_time, notification_type),
            title=self._generate_title(notification_type, task_title),
            message=self._generate_message(notification_type, task_title, task_start_time),
            scheduled_time=optimal_time,
            task_id=task_id,
            context_data={
                "task_title": task_title,
                "task_start_time": task_start_time.isoformat(),
                "user_productivity": self.behavior_analyzer.analyze_productivity_patterns()
            }
        )
        
        self.notifications_queue.append(notification)
        self.notifications_queue.sort(key=lambda x: x.scheduled_time)
    
    def _determine_priority(self, task_start_time: datetime, 
                          notification_type: NotificationType) -> NotificationPriority:
        """Определение приоритета уведомления"""
        time_until_task = task_start_time - datetime.now()
        
        if time_until_task.total_seconds() < 300:  # Менее 5 минут
            return NotificationPriority.URGENT
        elif time_until_task.total_seconds() < 900:  # Менее 15 минут
            return NotificationPriority.HIGH
        elif time_until_task.total_seconds() < 3600:  # Менее часа
            return NotificationPriority.MEDIUM
        else:
            return NotificationPriority.LOW
    
    def _generate_title(self, notification_type: NotificationType, task_title: str) -> str:
        """Генерация заголовка уведомления"""
        titles = {
            NotificationType.TASK_REMINDER: f"⏰ Напоминание: {task_title}",
            NotificationType.BREAK_SUGGESTION: "☕ Время для перерыва!",
            NotificationType.PRODUCTIVITY_ALERT: "📈 Анализ продуктивности",
            NotificationType.DEADLINE_WARNING: f"⚠️ Дедлайн приближается: {task_title}",
            NotificationType.FOCUS_TIME: "🎯 Время сосредоточиться",
            NotificationType.ACHIEVEMENT: "🏆 Достижение разблокировано!"
        }
        return titles.get(notification_type, "Уведомление")
    
    def _generate_message(self, notification_type: NotificationType, 
                         task_title: str, task_start_time: datetime) -> str:
        """Генерация текста уведомления"""
        time_str = task_start_time.strftime("%H:%M")
        
        messages = {
            NotificationType.TASK_REMINDER: f"Задача '{task_title}' запланирована на {time_str}. Готовы начать?",
            NotificationType.BREAK_SUGGESTION: "Вы работаете уже долго. Рекомендуем сделать 5-минутный перерыв.",
            NotificationType.PRODUCTIVITY_ALERT: "Ваша продуктивность снижается. Возможно, стоит пересмотреть план?",
            NotificationType.DEADLINE_WARNING: f"До дедлайна задачи '{task_title}' осталось мало времени!",
            NotificationType.FOCUS_TIME: "Сейчас ваше самое продуктивное время. Сосредоточьтесь на важных задачах!",
            NotificationType.ACHIEVEMENT: "Поздравляем! Вы достигли нового уровня продуктивности!"
        }
        return messages.get(notification_type, "У вас есть уведомление")
    
    def check_notifications(self):
        """Проверка и отправка уведомлений"""
        now = datetime.now()
        
        notifications_to_send = []
        for notification in self.notifications_queue[:]:
            if notification.scheduled_time <= now:
                notifications_to_send.append(notification)
                self.notifications_queue.remove(notification)
        
        for notification in notifications_to_send:
            self.send_notification(notification)
    
    def send_notification(self, notification: SmartNotification):
        """Отправка уведомления"""
        self.active_notifications[notification.id] = notification
        
        # Отправляем сигнал для UI
        self.notification_sent.emit(
            notification.title, 
            notification.message, 
            notification.type.value
        )
        
        # Системное уведомление
        if hasattr(self, 'tray_icon') and self.tray_icon:
            self.tray_icon.showMessage(
                notification.title,
                notification.message,
                QSystemTrayIcon.Information,
                5000  # 5 секунд
            )
    
    def handle_notification_response(self, notification_id: str, response: str):
        """Обработка ответа пользователя на уведомление"""
        if notification_id in self.active_notifications:
            notification = self.active_notifications[notification_id]
            notification.user_response = response
            
            # Записываем в анализатор поведения
            self.behavior_analyzer.record_notification_response(
                notification_id, response, 1.0  # время ответа
            )
            
            # Обновляем эффективность уведомления
            self._update_notification_effectiveness(notification, response)
            
            del self.active_notifications[notification_id]
    
    def _update_notification_effectiveness(self, notification: SmartNotification, response: str):
        """Обновление показателей эффективности уведомления"""
        effectiveness_scores = {
            "completed": 1.0,
            "snoozed": 0.7,
            "dismissed": 0.3,
            "ignored": 0.1
        }
        
        notification.effectiveness_score = effectiveness_scores.get(response, 0.5)
        
        # Здесь можно добавить машинное обучение для улучшения алгоритмов
    
    def get_productivity_insights(self) -> Dict:
        """Получение инсайтов о продуктивности"""
        patterns = self.behavior_analyzer.analyze_productivity_patterns()
        
        insights = {
            "best_hours": [],
            "best_days": [],
            "recommendations": []
        }
        
        # Лучшие часы
        hourly_sorted = sorted(patterns["hourly"].items(), 
                              key=lambda x: x[1], reverse=True)
        insights["best_hours"] = [f"{hour}:00" for hour, _ in hourly_sorted[:3]]
        
        # Лучшие дни
        days_names = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        weekly_sorted = sorted(patterns["weekly"].items(), 
                              key=lambda x: x[1], reverse=True)
        insights["best_days"] = [days_names[day] for day, _ in weekly_sorted[:3]]
        
        # Рекомендации
        insights["recommendations"] = self._generate_recommendations(patterns)
        
        return insights
    
    def _generate_recommendations(self, patterns: Dict) -> List[str]:
        """Генерация рекомендаций на основе паттернов"""
        recommendations = []
        
        # Анализ лучших часов
        best_hour = max(patterns["hourly"].items(), key=lambda x: x[1])
        if best_hour[1] > 0.8:
            recommendations.append(
                f"Ваша пиковая продуктивность в {best_hour[0]}:00. "
                f"Планируйте сложные задачи на это время."
            )
        
        # Анализ худших часов
        worst_hour = min(patterns["hourly"].items(), key=lambda x: x[1])
        if worst_hour[1] < 0.4:
            recommendations.append(
                f"В {worst_hour[0]}:00 ваша продуктивность снижается. "
                f"Используйте это время для перерывов."
            )
        
        return recommendations

# Глобальный экземпляр менеджера (ленивая инициализация)
_smart_notification_manager = None

def get_smart_notification_manager():
    """Получение глобального экземпляра менеджера с ленивой инициализацией"""
    global _smart_notification_manager
    if _smart_notification_manager is None:
        _smart_notification_manager = SmartNotificationManager()
    return _smart_notification_manager

# Для обратной совместимости
smart_notification_manager = None
