"""
🚀 Демонстрация улучшений Time Blocking приложения v6.0
Показывает все новые возможности и улучшения
"""

import sys
import asyncio
from datetime import datetime, timedelta
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Импорты наших улучшенных модулей
from config_manager import get_config, ConfigManager
from cache_manager import get_cache_manager, cached
from async_notifications import (
    get_notification_manager, create_task_reminder, 
    create_break_suggestion, create_deadline_warning
)
from modern_ui_components import (
    ModernButton, ModernCard, ModernTaskItem, 
    ModernSearchBox, ModernTabWidget, ModernSidebar, ModernStatusBar
)

class ImprovementsDemo(QMainWindow):
    """Демонстрация всех улучшений"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Time Blocking v6.0 - Демонстрация улучшений")
        self.setGeometry(100, 100, 1400, 900)
        
        # Инициализация компонентов
        self.config = get_config()
        self.cache = get_cache_manager()
        self.notifications = get_notification_manager()
        
        self._setup_ui()
        self._setup_demo_data()
        self._connect_signals()
        
        # Применяем современную тему
        self._apply_modern_theme()
    
    def _setup_ui(self):
        """Настройка интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Боковая панель
        self.sidebar = ModernSidebar()
        self.sidebar.add_item("🏠 Главная")
        self.sidebar.add_item("⚙️ Конфигурация")
        self.sidebar.add_item("💾 Кэширование")
        self.sidebar.add_item("🔔 Уведомления")
        self.sidebar.add_item("🎨 UI Компоненты")
        self.sidebar.add_item("📊 Статистика")
        main_layout.addWidget(self.sidebar)
        
        # Основная область
        self.content_area = QStackedWidget()
        main_layout.addWidget(self.content_area, 1)
        
        # Создаем страницы
        self._create_home_page()
        self._create_config_page()
        self._create_cache_page()
        self._create_notifications_page()
        self._create_ui_components_page()
        self._create_statistics_page()
        
        # Статус бар
        self.status_bar = ModernStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Выбираем первую страницу
        self.sidebar.select_item("🏠 Главная")
    
    def _create_home_page(self):
        """Создание главной страницы"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Заголовок
        title = QLabel("🚀 Time Blocking v6.0 - Улучшения")
        title.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #FF2B43;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(title)
        
        # Карточки с улучшениями
        improvements_layout = QGridLayout()
        
        # Карточка конфигурации
        config_card = ModernCard(
            "🔧 Система конфигурации",
            QLabel("Централизованное управление настройками\nс поддержкой переменных окружения")
        )
        improvements_layout.addWidget(config_card, 0, 0)
        
        # Карточка кэширования
        cache_card = ModernCard(
            "💾 Система кэширования",
            QLabel("Многоуровневое кэширование для\nулучшения производительности")
        )
        improvements_layout.addWidget(cache_card, 0, 1)
        
        # Карточка уведомлений
        notifications_card = ModernCard(
            "🔔 Асинхронные уведомления",
            QLabel("Умная система уведомлений\nс адаптивными алгоритмами")
        )
        improvements_layout.addWidget(notifications_card, 1, 0)
        
        # Карточка UI
        ui_card = ModernCard(
            "🎨 Современный UI",
            QLabel("Красивые компоненты интерфейса\nс анимациями и градиентами")
        )
        improvements_layout.addWidget(ui_card, 1, 1)
        
        layout.addLayout(improvements_layout)
        
        # Кнопки демонстрации
        demo_layout = QHBoxLayout()
        
        demo_config_btn = ModernButton("Показать конфигурацию", color="#4CAF50")
        demo_config_btn.clicked.connect(lambda: self._show_config_demo())
        demo_layout.addWidget(demo_config_btn)
        
        demo_cache_btn = ModernButton("Тест кэширования", color="#2196F3")
        demo_cache_btn.clicked.connect(lambda: self._show_cache_demo())
        demo_layout.addWidget(demo_cache_btn)
        
        demo_notifications_btn = ModernButton("Отправить уведомление", color="#FF9800")
        demo_notifications_btn.clicked.connect(lambda: self._show_notifications_demo())
        demo_layout.addWidget(demo_notifications_btn)
        
        layout.addLayout(demo_layout)
        layout.addStretch()
        
        self.content_area.addWidget(page)
    
    def _create_config_page(self):
        """Создание страницы конфигурации"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Заголовок
        title = QLabel("⚙️ Система конфигурации")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(title)
        
        # Текущая конфигурация
        config_text = QTextEdit()
        config_text.setReadOnly(True)
        config_text.setPlainText(self._get_config_info())
        layout.addWidget(config_text)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        reload_btn = ModernButton("🔄 Перезагрузить", color="#4CAF50")
        reload_btn.clicked.connect(self._reload_config)
        buttons_layout.addWidget(reload_btn)
        
        save_btn = ModernButton("💾 Сохранить", color="#2196F3")
        save_btn.clicked.connect(self._save_config)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
        
        self.content_area.addWidget(page)
    
    def _create_cache_page(self):
        """Создание страницы кэширования"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Заголовок
        title = QLabel("💾 Система кэширования")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(title)
        
        # Статистика кэша
        self.cache_stats_text = QTextEdit()
        self.cache_stats_text.setReadOnly(True)
        self._update_cache_stats()
        layout.addWidget(self.cache_stats_text)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        test_btn = ModernButton("🧪 Тест кэширования", color="#4CAF50")
        test_btn.clicked.connect(self._test_caching)
        buttons_layout.addWidget(test_btn)
        
        clear_btn = ModernButton("🗑️ Очистить кэш", color="#F44336")
        clear_btn.clicked.connect(self._clear_cache)
        buttons_layout.addWidget(clear_btn)
        
        refresh_btn = ModernButton("🔄 Обновить статистику", color="#2196F3")
        refresh_btn.clicked.connect(self._update_cache_stats)
        buttons_layout.addWidget(refresh_btn)
        
        layout.addLayout(buttons_layout)
        
        self.content_area.addWidget(page)
    
    def _create_notifications_page(self):
        """Создание страницы уведомлений"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Заголовок
        title = QLabel("🔔 Система уведомлений")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(title)
        
        # Статистика уведомлений
        self.notifications_stats_text = QTextEdit()
        self.notifications_stats_text.setReadOnly(True)
        self._update_notifications_stats()
        layout.addWidget(self.notifications_stats_text)
        
        # Кнопки тестирования
        buttons_layout = QGridLayout()
        
        reminder_btn = ModernButton("📅 Напоминание о задаче", color="#4CAF50")
        reminder_btn.clicked.connect(self._send_task_reminder)
        buttons_layout.addWidget(reminder_btn, 0, 0)
        
        break_btn = ModernButton("☕ Предложение перерыва", color="#FF9800")
        break_btn.clicked.connect(self._send_break_suggestion)
        buttons_layout.addWidget(break_btn, 0, 1)
        
        deadline_btn = ModernButton("⚠️ Предупреждение о дедлайне", color="#F44336")
        deadline_btn.clicked.connect(self._send_deadline_warning)
        buttons_layout.addWidget(deadline_btn, 1, 0)
        
        stats_btn = ModernButton("📊 Обновить статистику", color="#2196F3")
        stats_btn.clicked.connect(self._update_notifications_stats)
        buttons_layout.addWidget(stats_btn, 1, 1)
        
        layout.addLayout(buttons_layout)
        
        self.content_area.addWidget(page)
    
    def _create_ui_components_page(self):
        """Создание страницы UI компонентов"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Заголовок
        title = QLabel("🎨 Современные UI компоненты")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(title)
        
        # Демонстрация компонентов
        demo_layout = QGridLayout()
        
        # Кнопки
        buttons_card = ModernCard("Кнопки")
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(ModernButton("Обычная кнопка"))
        buttons_layout.addWidget(ModernButton("Успех", color="#4CAF50"))
        buttons_layout.addWidget(ModernButton("Предупреждение", color="#FF9800"))
        buttons_layout.addWidget(ModernButton("Ошибка", color="#F44336"))
        buttons_card.layout().addLayout(buttons_layout)
        demo_layout.addWidget(buttons_card, 0, 0)
        
        # Поиск
        search_card = ModernCard("Поиск")
        search_layout = QVBoxLayout()
        search_layout.addWidget(ModernSearchBox("Поиск задач..."))
        search_layout.addWidget(ModernSearchBox("Поиск проектов..."))
        search_card.layout().addLayout(search_layout)
        demo_layout.addWidget(search_card, 0, 1)
        
        # Задачи
        tasks_card = ModernCard("Элементы задач")
        tasks_layout = QVBoxLayout()
        
        sample_tasks = [
            {"id": "1", "title": "Завершить проект", "priority": "Высокий", "duration": 120, "progress": 75},
            {"id": "2", "title": "Встреча с командой", "priority": "Средний", "duration": 60, "progress": 0},
            {"id": "3", "title": "Код-ревью", "priority": "Низкий", "duration": 30, "progress": 100, "status": "completed"}
        ]
        
        for task_data in sample_tasks:
            task_item = ModernTaskItem(task_data)
            tasks_layout.addWidget(task_item)
        
        tasks_card.layout().addLayout(tasks_layout)
        demo_layout.addWidget(tasks_card, 1, 0, 1, 2)
        
        layout.addLayout(demo_layout)
        
        self.content_area.addWidget(page)
    
    def _create_statistics_page(self):
        """Создание страницы статистики"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Заголовок
        title = QLabel("📊 Статистика системы")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(title)
        
        # Общая статистика
        self.system_stats_text = QTextEdit()
        self.system_stats_text.setReadOnly(True)
        self._update_system_stats()
        layout.addWidget(self.system_stats_text)
        
        # Кнопка обновления
        refresh_btn = ModernButton("🔄 Обновить статистику", color="#2196F3")
        refresh_btn.clicked.connect(self._update_system_stats)
        layout.addWidget(refresh_btn)
        
        self.content_area.addWidget(page)
    
    def _setup_demo_data(self):
        """Настройка демонстрационных данных"""
        # Добавляем тестовые данные в кэш
        self.cache.set("demo_data", {"message": "Это тестовые данные в кэше"})
        self.cache.set("user_preferences", {"theme": "dark", "language": "ru"})
    
    def _connect_signals(self):
        """Подключение сигналов"""
        self.sidebar.item_clicked.connect(self._on_sidebar_item_clicked)
        
        # Подключаем сигналы уведомлений
        self.notifications.notification_sent.connect(self._on_notification_sent)
        self.notifications.notification_failed.connect(self._on_notification_failed)
    
    def _apply_modern_theme(self):
        """Применение современной темы"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
            }
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
    
    # Обработчики событий
    
    def _on_sidebar_item_clicked(self, item_name: str):
        """Обработка клика по элементу боковой панели"""
        index_map = {
            "🏠 Главная": 0,
            "⚙️ Конфигурация": 1,
            "💾 Кэширование": 2,
            "🔔 Уведомления": 3,
            "🎨 UI Компоненты": 4,
            "📊 Статистика": 5
        }
        
        if item_name in index_map:
            self.content_area.setCurrentIndex(index_map[item_name])
            self.status_bar.status_label.setText(f"Открыта страница: {item_name}")
    
    def _on_notification_sent(self, notification_id: str):
        """Обработка отправленного уведомления"""
        self.status_bar.status_label.setText(f"Уведомление {notification_id} отправлено")
    
    def _on_notification_failed(self, notification_id: str, error: str):
        """Обработка ошибки уведомления"""
        self.status_bar.status_label.setText(f"Ошибка уведомления {notification_id}: {error}")
    
    # Демонстрационные методы
    
    def _show_config_demo(self):
        """Демонстрация конфигурации"""
        config_info = f"""
Текущая конфигурация:
- Язык: {self.config.ui.language}
- Тема: {self.config.ui.theme}
- Анимации: {self.config.ui.animations_enabled}
- ИИ провайдер: {self.config.ai.provider}
- Кэширование: {self.config.data.cache_enabled}
        """
        QMessageBox.information(self, "Конфигурация", config_info.strip())
    
    def _show_cache_demo(self):
        """Демонстрация кэширования"""
        # Тестируем кэш
        import time
        start_time = time.time()
        
        # Сохраняем данные
        test_data = {"timestamp": datetime.now().isoformat(), "data": list(range(1000))}
        self.cache.set("performance_test", test_data)
        
        # Читаем данные
        cached_data = self.cache.get("performance_test")
        
        end_time = time.time()
        
        result = f"""
Тест кэширования завершен:
- Время выполнения: {(end_time - start_time) * 1000:.2f} мс
- Данные сохранены: {len(test_data['data'])} элементов
- Данные прочитаны: {'Успешно' if cached_data else 'Ошибка'}
        """
        QMessageBox.information(self, "Тест кэширования", result.strip())
    
    def _show_notifications_demo(self):
        """Демонстрация уведомлений"""
        notification = create_task_reminder(
            "demo_task",
            "Демонстрационная задача",
            datetime.now()
        )
        self.notifications.send_notification_sync(notification)
    
    # Методы обновления данных
    
    def _get_config_info(self) -> str:
        """Получение информации о конфигурации"""
        return f"""
Конфигурация приложения Time Blocking v6.0

UI настройки:
- Язык интерфейса: {self.config.ui.language}
- Тема: {self.config.ui.theme}
- Анимации включены: {self.config.ui.animations_enabled}
- Размер окна: {self.config.ui.window_width}x{self.config.ui.window_height}
- Интервал автосохранения: {self.config.ui.auto_save_interval} сек
- Размер шрифта: {self.config.ui.font_size}
- Показывать уведомления: {self.config.ui.show_notifications}

ИИ настройки:
- Провайдер: {self.config.ai.provider}
- Модель: {self.config.ai.model}
- Максимум токенов: {self.config.ai.max_tokens}
- Температура: {self.config.ai.temperature}
- Офлайн режим: {self.config.ai.offline_mode}
- Максимум попыток: {self.config.ai.max_retries}

Данные:
- Резервное копирование: {self.config.data.backup_enabled}
- Интервал резервирования: {self.config.data.backup_interval_hours} ч
- Облачная синхронизация: {self.config.data.cloud_sync}
- Формат экспорта: {self.config.data.export_format}
- Хранение данных: {self.config.data.data_retention_days} дней
- Кэширование: {self.config.data.cache_enabled}
- Размер кэша: {self.config.data.cache_size_mb} МБ

Производительность:
- Асинхронные операции: {self.config.performance.async_operations}
- Максимум задач: {self.config.performance.max_concurrent_tasks}
- Интервал обновления UI: {self.config.performance.ui_update_interval_ms} мс
- Интервал аналитики: {self.config.performance.analytics_update_interval_ms} мс
- Ленивая загрузка: {self.config.performance.lazy_loading}
- Лимит памяти: {self.config.performance.memory_limit_mb} МБ

Отладка:
- Режим отладки: {self.config.debug_mode}
- Уровень логирования: {self.config.log_level}
        """
    
    def _reload_config(self):
        """Перезагрузка конфигурации"""
        self.config = get_config()
        self.status_bar.status_label.setText("Конфигурация перезагружена")
    
    def _save_config(self):
        """Сохранение конфигурации"""
        from config_manager import save_config
        if save_config():
            self.status_bar.status_label.setText("Конфигурация сохранена")
        else:
            self.status_bar.status_label.setText("Ошибка сохранения конфигурации")
    
    def _update_cache_stats(self):
        """Обновление статистики кэша"""
        stats = self.cache.get_stats()
        
        stats_text = f"""
Статистика кэширования:

Кэш в памяти:
- Размер: {stats['memory_cache']['size']} / {stats['memory_cache']['max_size']} элементов
- Попадания: {stats['memory_cache']['hits']}
- Промахи: {stats['memory_cache']['misses']}
- Вытеснения: {stats['memory_cache']['evictions']}
- Процент попаданий: {stats['memory_cache']['hit_rate']:.1f}%

Файловый кэш:
- Директория: {stats['file_cache_dir']}
- Максимальный размер: {stats['file_cache_size_mb']:.1f} МБ

Обновлено: {datetime.now().strftime('%H:%M:%S')}
        """
        
        self.cache_stats_text.setPlainText(stats_text.strip())
    
    def _test_caching(self):
        """Тестирование кэширования"""
        self.status_bar.show_progress("Тестирование кэша...")
        
        # Имитируем тяжелую операцию
        QTimer.singleShot(1000, self._complete_cache_test)
    
    def _complete_cache_test(self):
        """Завершение теста кэширования"""
        import time
        
        # Тест производительности
        start_time = time.time()
        
        # Записываем 100 элементов
        for i in range(100):
            self.cache.set(f"test_key_{i}", f"test_value_{i}")
        
        # Читаем 100 элементов
        for i in range(100):
            self.cache.get(f"test_key_{i}")
        
        end_time = time.time()
        
        self.status_bar.hide_progress()
        self.status_bar.status_label.setText(
            f"Тест кэша завершен за {(end_time - start_time) * 1000:.1f} мс"
        )
        
        self._update_cache_stats()
    
    def _clear_cache(self):
        """Очистка кэша"""
        self.cache.clear()
        self.status_bar.status_label.setText("Кэш очищен")
        self._update_cache_stats()
    
    def _update_notifications_stats(self):
        """Обновление статистики уведомлений"""
        stats = self.notifications.get_statistics()
        
        stats_text = f"""
Статистика уведомлений:

Общая информация:
- Всего отправлено: {stats.get('total', 0)}
- Доставлено успешно: {stats.get('delivered', 0)}
- Процент доставки: {stats.get('delivery_rate', 0):.1f}%
- В очереди: {stats.get('queue_size', 0)}
- Запланировано: {stats.get('scheduled_count', 0)}

По типам:
"""
        
        for type_name, count in stats.get('by_type', {}).items():
            stats_text += f"- {type_name}: {count}\n"
        
        stats_text += "\nПо приоритетам:\n"
        for priority, count in stats.get('by_priority', {}).items():
            stats_text += f"- {priority}: {count}\n"
        
        stats_text += f"\nОбновлено: {datetime.now().strftime('%H:%M:%S')}"
        
        self.notifications_stats_text.setPlainText(stats_text.strip())
    
    def _send_task_reminder(self):
        """Отправка напоминания о задаче"""
        notification = create_task_reminder(
            "demo_task_1",
            "Завершить демонстрацию улучшений",
            datetime.now()
        )
        self.notifications.send_notification_sync(notification)
    
    def _send_break_suggestion(self):
        """Отправка предложения перерыва"""
        notification = create_break_suggestion(90)  # 90 минут работы
        self.notifications.send_notification_sync(notification)
    
    def _send_deadline_warning(self):
        """Отправка предупреждения о дедлайне"""
        notification = create_deadline_warning("Демонстрационный проект", 2)  # 2 часа до дедлайна
        self.notifications.send_notification_sync(notification)
    
    def _update_system_stats(self):
        """Обновление системной статистики"""
        import psutil
        import platform
        
        # Системная информация
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        stats_text = f"""
Системная статистика Time Blocking v6.0:

Система:
- Платформа: {platform.system()} {platform.release()}
- Архитектура: {platform.machine()}
- Python: {platform.python_version()}

Ресурсы:
- CPU: {cpu_percent}%
- Память: {memory.percent}% ({memory.used // (1024**3):.1f} / {memory.total // (1024**3):.1f} ГБ)
- Диск: {disk.percent}% ({disk.used // (1024**3):.1f} / {disk.total // (1024**3):.1f} ГБ)

Кэш:
- Элементов в памяти: {self.cache.get_stats()['memory_cache']['size']}
- Процент попаданий: {self.cache.get_stats()['memory_cache']['hit_rate']:.1f}%

Уведомления:
- Всего отправлено: {self.notifications.get_statistics().get('total', 0)}
- В очереди: {self.notifications.get_statistics().get('queue_size', 0)}

Обновлено: {datetime.now().strftime('%H:%M:%S')}
        """
        
        self.system_stats_text.setPlainText(stats_text.strip())

def main():
    """Главная функция"""
    app = QApplication(sys.argv)
    
    # Устанавливаем иконку приложения
    app.setWindowIcon(app.style().standardIcon(QStyle.SP_ComputerIcon))
    
    # Создаем и показываем окно
    window = ImprovementsDemo()
    window.show()
    
    # Запускаем приложение
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
