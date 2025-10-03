# safe_launch.py - Безопасный запуск приложения без ошибок таймеров
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QTabWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

# Импорты основных модулей
try:
    from localization_system import localization, _
    from task_manager import task_manager, Task, TaskStatus, TaskPriority
    CORE_MODULES_AVAILABLE = True
    print("✅ Основные модули успешно загружены")
except ImportError as e:
    print(f"❌ Ошибка импорта основных модулей: {e}")
    CORE_MODULES_AVAILABLE = False
    
    # Создаем заглушки для работы без основных модулей
    def _(text):
        return text
    
    class MockTaskManager:
        def get_all_tasks(self):
            return []
        def calculate_productivity_today(self):
            return {'productivity_percent': 0, 'total_tasks': 0}
    
    task_manager = MockTaskManager()

class SafeTimeBlockingApp(QMainWindow):
    """Безопасная версия приложения без проблем с таймерами"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 Time Blocking v4.0 - Безопасный режим")
        self.setGeometry(100, 100, 1200, 800)
        
        # Инициализация UI
        self.init_ui()
        
        # Инициализация улучшенных модулей после создания UI
        self.init_enhanced_features()
    
    def init_ui(self):
        """Инициализация базового интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Заголовок
        header = QLabel("⏰ Time Blocking Application v4.0")
        header.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #FF2B43;
            padding: 20px;
            text-align: center;
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Статус модулей
        self.status_label = QLabel("🔄 Инициализация модулей...")
        self.status_label.setStyleSheet("""
            background: #2D2D2D;
            padding: 15px;
            border-radius: 8px;
            color: #CCCCCC;
            font-size: 14px;
        """)
        layout.addWidget(self.status_label)
        
        # Вкладки
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #FF2B43;
                border-radius: 8px;
                background: #1E1E1E;
            }
            QTabBar::tab {
                background: #2D2D2D;
                color: white;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: #FF2B43;
            }
        """)
        
        # Основная вкладка
        main_tab = self.create_main_tab()
        self.tabs.addTab(main_tab, "📋 Главная")
        
        # Вкладка аналитики (будет добавлена позже)
        analytics_placeholder = QLabel("📊 Продвинутая аналитика загружается...")
        analytics_placeholder.setAlignment(Qt.AlignCenter)
        analytics_placeholder.setStyleSheet("color: #888; font-size: 16px; padding: 50px;")
        self.tabs.addTab(analytics_placeholder, "📊 Аналитика")
        
        layout.addWidget(self.tabs)
        
        # Применяем темную тему
        self.setStyleSheet("""
            QMainWindow {
                background: #1E1E1E;
                color: white;
            }
            QWidget {
                background: #1E1E1E;
                color: white;
            }
            QPushButton {
                background: #FF2B43;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 120px;
                min-height: 40px;
            }
            QPushButton:hover {
                background: #FF4A5F;
            }
        """)
    
    def create_main_tab(self):
        """Создание главной вкладки"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Информация о новых функциях
        info_text = """
🎉 Добро пожаловать в Time Blocking v4.0!

✨ Новые возможности:
• 🧠 Умные уведомления с машинным обучением
• 📊 Тепловая карта продуктивности
• 🎨 Drag & Drop интерфейс
• ☁️ Облачная синхронизация
• ⚡ Оптимизация производительности

🚀 Статус загрузки модулей:
"""
        
        info_label = QLabel(info_text)
        info_label.setStyleSheet("""
            background: rgba(255, 43, 67, 0.1);
            border: 2px solid #FF2B43;
            border-radius: 10px;
            padding: 20px;
            color: white;
            font-size: 14px;
            line-height: 1.6;
        """)
        layout.addWidget(info_label)
        
        # Кнопки действий
        buttons_layout = QHBoxLayout()
        
        # Кнопка запуска полной версии
        full_version_btn = QPushButton("🚀 Запустить полную версию")
        full_version_btn.clicked.connect(self.launch_full_version)
        
        # Кнопка тестирования аналитики
        test_analytics_btn = QPushButton("📊 Тест аналитики")
        test_analytics_btn.clicked.connect(self.test_analytics)
        
        # Кнопка настроек
        settings_btn = QPushButton("⚙️ Настройки")
        settings_btn.clicked.connect(self.show_settings)
        
        buttons_layout.addWidget(full_version_btn)
        buttons_layout.addWidget(test_analytics_btn)
        buttons_layout.addWidget(settings_btn)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def init_enhanced_features(self):
        """Безопасная инициализация улучшенных функций"""
        status_messages = []
        
        try:
            # Проверяем доступность основных модулей
            if CORE_MODULES_AVAILABLE:
                status_messages.append("✅ Основные модули: загружены")
                
                # Показываем информацию о задачах
                try:
                    tasks = task_manager.get_all_tasks()
                    productivity = task_manager.calculate_productivity_today()
                    status_messages.append(f"📋 Задач всего: {len(tasks)}")
                    status_messages.append(f"📊 Продуктивность сегодня: {productivity.get('productivity_percent', 0)}%")
                except Exception as e:
                    status_messages.append(f"⚠️ Ошибка получения данных задач: {e}")
            else:
                status_messages.append("⚠️ Основные модули: ошибка загрузки")
            
            # Пытаемся загрузить улучшенные модули
            self.smart_notifications = None
            self.analytics_widget = None
            self.performance_optimizer = None
            
            # Умные уведомления
            try:
                from smart_notifications import get_smart_notification_manager
                self.smart_notifications = get_smart_notification_manager()
                status_messages.append("✅ Умные уведомления: активны")
            except ImportError as e:
                if "matplotlib" in str(e) or "numpy" in str(e) or "pandas" in str(e):
                    status_messages.append("⚠️ Умные уведомления: требуется установка зависимостей")
                    status_messages.append("   pip install matplotlib numpy pandas")
                else:
                    status_messages.append(f"⚠️ Умные уведомления: {str(e)[:40]}...")
            except Exception as e:
                status_messages.append(f"⚠️ Умные уведомления: {str(e)[:40]}...")
            
            # Продвинутая аналитика
            try:
                from advanced_analytics import get_advanced_analytics_widget
                self.analytics_widget = get_advanced_analytics_widget()
                status_messages.append("✅ Продвинутая аналитика: загружена")
                
                # Заменяем placeholder на реальный виджет
                if self.analytics_widget:
                    self.tabs.removeTab(1)
                    self.tabs.insertTab(1, self.analytics_widget, "📊 Аналитика")
                    
            except ImportError as e:
                if "matplotlib" in str(e) or "seaborn" in str(e):
                    status_messages.append("⚠️ Аналитика: требуется matplotlib и seaborn")
                    status_messages.append("   pip install matplotlib seaborn")
                else:
                    status_messages.append(f"⚠️ Аналитика: {str(e)[:40]}...")
            except Exception as e:
                status_messages.append(f"⚠️ Аналитика: {str(e)[:40]}...")
            
            # Оптимизация производительности
            try:
                from performance_optimizer import get_performance_optimizer
                self.performance_optimizer = get_performance_optimizer()
                status_messages.append("✅ Оптимизация: включена")
            except Exception as e:
                status_messages.append(f"⚠️ Оптимизация: {str(e)[:40]}...")
            
            # Обновляем статус
            status_text = "\n".join(status_messages)
            self.status_label.setText(f"📊 Статус модулей:\n{status_text}")
            
            # Добавляем инструкции по установке зависимостей
            if any("требуется" in msg for msg in status_messages):
                self.add_installation_instructions()
            
        except Exception as e:
            self.status_label.setText(f"❌ Критическая ошибка инициализации: {e}")
    
    def add_installation_instructions(self):
        """Добавление инструкций по установке"""
        instructions_text = """
🔧 Для полной функциональности установите зависимости:

pip install matplotlib seaborn numpy pandas requests dropbox openpyxl reportlab

После установки перезапустите приложение.
        """
        
        instructions_label = QLabel(instructions_text)
        instructions_label.setStyleSheet("""
            background: rgba(255, 193, 7, 0.1);
            border: 2px solid #FFC107;
            border-radius: 8px;
            padding: 15px;
            color: #FFC107;
            font-size: 12px;
        """)
        
        # Добавляем в основную вкладку
        main_tab = self.tabs.widget(0)
        if main_tab and hasattr(main_tab, 'layout'):
            main_tab.layout().addWidget(instructions_label)
    
    def launch_full_version(self):
        """Запуск полной версии приложения"""
        try:
            from hybrid_app import HybridTimeBlockingApp
            self.full_app = HybridTimeBlockingApp()
            self.full_app.show()
            self.status_label.setText("🚀 Полная версия запущена в отдельном окне!")
        except Exception as e:
            self.status_label.setText(f"❌ Ошибка запуска полной версии: {e}")
    
    def test_analytics(self):
        """Тестирование аналитики"""
        if self.analytics_widget:
            self.tabs.setCurrentIndex(1)
            self.status_label.setText("📊 Переключение на вкладку аналитики...")
        else:
            self.status_label.setText("⚠️ Модуль аналитики недоступен")
    
    def show_settings(self):
        """Показать настройки"""
        self.status_label.setText("⚙️ Настройки будут добавлены в следующей версии")

def main():
    """Безопасная главная функция"""
    app = QApplication(sys.argv)
    
    print("🚀 Запуск Time Blocking v4.0 в безопасном режиме...")
    print("🔧 Это исправляет ошибки с QTimer и потоками")
    
    # Создаем и показываем приложение
    window = SafeTimeBlockingApp()
    window.show()
    
    print("✅ Приложение успешно запущено!")
    print("💡 Если возникнут проблемы, используйте этот безопасный режим")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
