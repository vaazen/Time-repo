# modern_settings.py - Современная система настроек Time Blocking v5.0
import json
import os
from PyQt5.QtCore import QSettings, Qt, pyqtSignal
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QGroupBox, QCheckBox, QComboBox, QSpinBox, 
                             QLineEdit, QPushButton, QDialogButtonBox, QLabel, 
                             QTabWidget, QWidget, QSlider, QMessageBox, 
                             QTextEdit, QFrame)
from PyQt5.QtGui import QFont, QColor

class ModernSettings:
    """Современный менеджер настроек"""
    
    def __init__(self):
        self.settings = QSettings("TimeBlocking", "v5.0")
        self.defaults = {
            "general/language": "ru",
            "general/theme": "dark",
            "general/first_run": True,
            
            "appearance/font_size": 12,
            "appearance/font_family": "Segoe UI",
            "appearance/animations": True,
            
            "ai/enabled": True,
            "ai/provider": "openai",
            "ai/api_key": "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",
            "ai/model": "gpt-3.5-turbo",
            
            "integrations/slack_enabled": False,
            "integrations/slack_webhook": "",
            "integrations/trello_enabled": False,
            "integrations/trello_key": "",
            "integrations/notion_enabled": False,
            "integrations/notion_token": ""
        }
    
    def get(self, key, default=None):
        if key in self.defaults:
            default = self.defaults[key]
        return self.settings.value(key, default)
    
    def set(self, key, value):
        self.settings.setValue(key, value)
        self.settings.sync()
    
    def reset_to_defaults(self):
        self.settings.clear()
        self.settings.sync()

class ModernSettingsDialog(QDialog):
    """Современный диалог настроек"""
    settings_changed = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = ModernSettings()
        self.setWindowTitle("⚙️ Настройки Time Blocking v5.0")
        self.setFixedSize(900, 700)
        self.setup_ui()
        self.load_settings()
        self.apply_modern_style()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Заголовок
        header = QLabel("⚙️ Настройки Time Blocking v5.0")
        header.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            padding: 15px; 
            color: #FF2B43;
            text-align: center;
        """)
        layout.addWidget(header)
        
        # Вкладки
        self.tabs = QTabWidget()
        
        # Создаем вкладки
        self.tabs.addTab(self.create_general_tab(), "🌐 Общие")
        self.tabs.addTab(self.create_ai_tab(), "🤖 ИИ-Помощник") 
        self.tabs.addTab(self.create_integrations_tab(), "🔗 Интеграции")
        self.tabs.addTab(self.create_about_tab(), "ℹ️ О программе")
        
        layout.addWidget(self.tabs)
        
        # Кнопки
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply
        )
        buttons.accepted.connect(self.save_and_close)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.Apply).clicked.connect(self.apply_settings)
        layout.addWidget(buttons)
    
    def create_general_tab(self):
        """Вкладка общих настроек"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Язык интерфейса
        lang_group = QGroupBox("🌐 Язык интерфейса")
        lang_layout = QFormLayout(lang_group)
        
        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "🇷🇺 Русский", 
            "🇺🇸 English", 
            "🇩🇪 Deutsch",
            "🇫🇷 Français",
            "🇪🇸 Español"
        ])
        lang_layout.addRow("Выберите язык:", self.language_combo)
        
        restart_note = QLabel("⚠️ Требуется перезапуск для применения изменений")
        restart_note.setStyleSheet("color: #FF9800; font-style: italic; font-size: 11px;")
        lang_layout.addRow(restart_note)
        
        # Тема оформления
        theme_group = QGroupBox("🎨 Внешний вид")
        theme_layout = QFormLayout(theme_group)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["🌙 Темная", "☀️ Светлая", "🔄 Авто"])
        theme_layout.addRow("Тема:", self.theme_combo)
        
        self.font_size = QSpinBox()
        self.font_size.setRange(10, 20)
        self.font_size.setValue(12)
        self.font_size.setSuffix(" px")
        theme_layout.addRow("Размер шрифта:", self.font_size)
        
        # Поведение приложения
        behavior_group = QGroupBox("⚙️ Поведение")
        behavior_layout = QFormLayout(behavior_group)
        
        self.start_with_system = QCheckBox("Запускать с системой")
        behavior_layout.addRow(self.start_with_system)
        
        self.minimize_to_tray = QCheckBox("Сворачивать в трей")
        self.minimize_to_tray.setChecked(True)
        behavior_layout.addRow(self.minimize_to_tray)
        
        layout.addWidget(lang_group)
        layout.addWidget(theme_group)
        layout.addWidget(behavior_group)
        layout.addStretch()
        
        return widget
    
    def create_ai_tab(self):
        """Вкладка настроек ИИ-помощника"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Основные настройки ИИ
        ai_group = QGroupBox("🤖 ИИ-Помощник")
        ai_layout = QFormLayout(ai_group)
        
        self.ai_enabled = QCheckBox("Включить ИИ-помощника")
        self.ai_enabled.setChecked(True)
        ai_layout.addRow(self.ai_enabled)
        
        self.ai_provider = QComboBox()
        self.ai_provider.addItems(["OpenAI GPT", "DeepSeek", "Офлайн режим"])
        ai_layout.addRow("Провайдер ИИ:", self.ai_provider)
        
        # API настройки
        api_group = QGroupBox("🔑 API настройки")
        api_layout = QFormLayout(api_group)
        
        self.api_key = QLineEdit()
        self.api_key.setPlaceholderText("Введите API ключ...")
        self.api_key.setText("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")
        self.api_key.setEchoMode(QLineEdit.Password)
        api_layout.addRow("API ключ:", self.api_key)
        
        show_key_btn = QPushButton("👁️ Показать")
        show_key_btn.setCheckable(True)
        show_key_btn.toggled.connect(lambda checked: self.api_key.setEchoMode(
            QLineEdit.Normal if checked else QLineEdit.Password))
        api_layout.addRow("", show_key_btn)
        
        self.model_combo = QComboBox()
        self.model_combo.addItems(["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"])
        api_layout.addRow("Модель:", self.model_combo)
        
        # Поведение ИИ
        behavior_group = QGroupBox("🧠 Поведение ИИ")
        behavior_layout = QFormLayout(behavior_group)
        
        self.auto_analyze = QCheckBox("Автоматический анализ задач")
        self.auto_analyze.setChecked(True)
        behavior_layout.addRow(self.auto_analyze)
        
        self.smart_suggestions = QCheckBox("Умные предложения")
        self.smart_suggestions.setChecked(True)
        behavior_layout.addRow(self.smart_suggestions)
        
        layout.addWidget(ai_group)
        layout.addWidget(api_group)
        layout.addWidget(behavior_group)
        layout.addStretch()
        
        return widget
    
    def create_integrations_tab(self):
        """Вкладка интеграций с внешними сервисами"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Slack
        slack_group = QGroupBox("📱 Slack")
        slack_layout = QFormLayout(slack_group)
        
        self.slack_enabled = QCheckBox("Включить интеграцию со Slack")
        slack_layout.addRow(self.slack_enabled)
        
        self.slack_webhook = QLineEdit()
        self.slack_webhook.setPlaceholderText("https://hooks.slack.com/services/...")
        slack_layout.addRow("Webhook URL:", self.slack_webhook)
        
        self.slack_channel = QLineEdit()
        self.slack_channel.setPlaceholderText("#general")
        self.slack_channel.setText("#general")
        slack_layout.addRow("Канал:", self.slack_channel)
        
        test_slack_btn = QPushButton("🧪 Тест")
        test_slack_btn.clicked.connect(self.test_slack)
        slack_layout.addRow("", test_slack_btn)
        
        # Trello
        trello_group = QGroupBox("📋 Trello")
        trello_layout = QFormLayout(trello_group)
        
        self.trello_enabled = QCheckBox("Включить интеграцию с Trello")
        trello_layout.addRow(self.trello_enabled)
        
        self.trello_key = QLineEdit()
        self.trello_key.setPlaceholderText("API Key от Trello")
        trello_layout.addRow("API Key:", self.trello_key)
        
        self.trello_token = QLineEdit()
        self.trello_token.setPlaceholderText("Token от Trello")
        trello_layout.addRow("Token:", self.trello_token)
        
        get_trello_btn = QPushButton("🔗 Получить ключи")
        get_trello_btn.clicked.connect(lambda: os.system("start https://trello.com/app-key"))
        trello_layout.addRow("", get_trello_btn)
        
        # Notion
        notion_group = QGroupBox("📝 Notion")
        notion_layout = QFormLayout(notion_group)
        
        self.notion_enabled = QCheckBox("Включить интеграцию с Notion")
        notion_layout.addRow(self.notion_enabled)
        
        self.notion_token = QLineEdit()
        self.notion_token.setPlaceholderText("Integration Token")
        notion_layout.addRow("Token:", self.notion_token)
        
        get_notion_btn = QPushButton("🔗 Создать интеграцию")
        get_notion_btn.clicked.connect(lambda: os.system("start https://www.notion.so/my-integrations"))
        notion_layout.addRow("", get_notion_btn)
        
        layout.addWidget(slack_group)
        layout.addWidget(trello_group)
        layout.addWidget(notion_group)
        layout.addStretch()
        
        return widget
    
    def create_about_tab(self):
        """Вкладка о программе и команде разработчиков"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Информация о программе
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setHtml("""
        <div style='font-family: Segoe UI; padding: 20px; line-height: 1.6;'>
            <div style='text-align: center; margin-bottom: 30px;'>
                <h1 style='color: #FF2B43; margin-bottom: 10px; font-size: 28px;'>🚀 Time Blocking v5.0</h1>
                <h2 style='color: #888; margin-bottom: 20px; font-size: 18px;'>ИИ-Революция в планировании!</h2>
                
                <div style='background: #2A2A2A; padding: 15px; border-radius: 8px; margin: 20px auto; max-width: 400px;'>
                    <p style='margin: 5px 0;'><b>Версия:</b> 5.0.0 (Октябрь 2024)</p>
                    <p style='margin: 5px 0;'><b>Лицензия:</b> MIT License</p>
                    <p style='margin: 5px 0;'><b>Платформа:</b> Windows, macOS, Linux</p>
                </div>
            </div>
            
            <hr style='border: 1px solid #444; margin: 30px 0;'>
            
            <h3 style='color: #FF2B43; text-align: center; margin-bottom: 25px; font-size: 20px;'>👥 Команда разработчиков</h3>
            
            <div style='max-width: 600px; margin: 0 auto;'>
                <div style='background: #1E1E1E; padding: 20px; border-radius: 12px; margin: 15px 0; border-left: 4px solid #FF2B43;'>
                    <h4 style='color: #FF2B43; margin: 0 0 10px 0; font-size: 16px;'>🧑‍💻 Главный разработчик</h4>
                    <p style='margin: 8px 0; font-size: 14px;'><b>Костя, Макс, Влад, Саша</b> (@vaazen, @Max111111m, @Vladislav122312, @dr1ms0n)</p>
                    <p style='color: #AAA; margin: 0; font-style: italic; font-size: 13px;'>
                        Архитектура приложения • ИИ-интеграция • UI/UX дизайн • Управление проектом
                    </p>
                </div>
                
                <div style='background: #1E1E1E; padding: 20px; border-radius: 12px; margin: 15px 0; border-left: 4px solid #4CAF50;'>
                    <h4 style='color: #4CAF50; margin: 0 0 10px 0; font-size: 16px;'>🤖 ИИ-Ассистент</h4>
                    <p style='margin: 8px 0; font-size: 14px;'><b>Cascade AI</b> (Windsurf Platform)</p>
                    <p style='color: #AAA; margin: 0; font-style: italic; font-size: 13px;'>
                        Разработка модулей • Оптимизация кода • Автоматизация • Тестирование
                    </p>
                </div>
                
                <div style='background: #1E1E1E; padding: 20px; border-radius: 12px; margin: 15px 0; border-left: 4px solid #2196F3;'>
                    <h4 style='color: #2196F3; margin: 0 0 10px 0; font-size: 16px;'>🎨 Дизайн и UX</h4>
                    <p style='margin: 8px 0; font-size: 14px;'><b>Modern Material Design</b></p>
                    <p style='color: #AAA; margin: 0; font-style: italic; font-size: 13px;'>
                        Темная тема • Анимации • Адаптивный интерфейс • Иконография
                    </p>
                </div>
                
                <div style='background: #1E1E1E; padding: 20px; border-radius: 12px; margin: 15px 0; border-left: 4px solid #9C27B0;'>
                    <h4 style='color: #9C27B0; margin: 0 0 10px 0; font-size: 16px;'>🔗 Интеграции</h4>
                    <p style='margin: 8px 0; font-size: 14px;'><b>OpenAI • Slack • Trello • Notion</b></p>
                    <p style='color: #AAA; margin: 0; font-style: italic; font-size: 13px;'>
                        API интеграции • Облачная синхронизация • Автоматизация рабочих процессов
                    </p>
                </div>
            </div>
            
            <hr style='border: 1px solid #444; margin: 30px 0;'>
            
            <div style='text-align: center;'>
                <div style='background: #2A2A2A; padding: 20px; border-radius: 12px; margin: 20px auto; max-width: 500px;'>
                    <h3 style='color: #FF2B43; margin-bottom: 15px; font-size: 18px;'>📞 Контакты и поддержка</h3>
                    <p style='margin: 8px 0; font-size: 14px;'>📧 <b>Email:</b> kostybaz@gmail.com</p>
                    <p style='margin: 8px 0; font-size: 14px;'>💬 <b>Telegram:</b> @vaazen</p>
                    <p style='margin: 8px 0; font-size: 14px;'>🐛 <b>GitHub:</b> github.com/vaazen</p>
                    <p style='margin: 8px 0; font-size: 14px;'>🌐 <b>Сайт:</b> timeblocking.app</p>
                </div>
                
                <div style='margin-top: 30px; color: #666; font-size: 12px;'>
                    <p style='margin: 5px 0;'>Создано с ❤️ и 🤖 ИИ для максимальной продуктивности</p>
                    <p style='margin: 5px 0;'>© 2024 Time Blocking Team. Все права защищены.</p>
                </div>
            </div>
        </div>
        """)
        
        layout.addWidget(about_text)
        
        return widget
    
    def load_settings(self):
        """Загрузка настроек из файла"""
        # Язык
        lang_map = {"ru": 0, "en": 1, "de": 2, "fr": 3, "es": 4}
        current_lang = self.settings.get("general/language", "ru")
        self.language_combo.setCurrentIndex(lang_map.get(current_lang, 0))
        
        # ИИ настройки
        self.ai_enabled.setChecked(self.settings.get("ai/enabled", True))
        self.api_key.setText(self.settings.get("ai/api_key", ""))
        
        # Интеграции
        self.slack_enabled.setChecked(self.settings.get("integrations/slack_enabled", False))
        self.slack_webhook.setText(self.settings.get("integrations/slack_webhook", ""))
    
    def apply_settings(self):
        """Применение настроек"""
        # Сохраняем язык
        lang_values = ["ru", "en", "de", "fr", "es"]
        self.settings.set("general/language", lang_values[self.language_combo.currentIndex()])
        
        # Сохраняем ИИ настройки
        self.settings.set("ai/enabled", self.ai_enabled.isChecked())
        self.settings.set("ai/api_key", self.api_key.text())
        
        # Сохраняем интеграции
        self.settings.set("integrations/slack_enabled", self.slack_enabled.isChecked())
        self.settings.set("integrations/slack_webhook", self.slack_webhook.text())
        
        self.settings_changed.emit({})
    
    def save_and_close(self):
        """Сохранить и закрыть"""
        self.apply_settings()
        self.accept()
    
    def test_slack(self):
        """Тест интеграции со Slack"""
        QMessageBox.information(self, "Тест Slack", 
                               "Функция тестирования Slack будет добавлена в следующем обновлении!")
    
    def apply_modern_style(self):
        """Применение современного стиля"""
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1A1A1A, stop:1 #2A2A2A);
                color: white;
            }
            QGroupBox {
                color: #FF2B43;
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #444;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background: #FF2B43;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                min-height: 30px;
            }
            QPushButton:hover {
                background: #FF4A5F;
            }
            QPushButton:pressed {
                background: #E01E37;
            }
            QLineEdit {
                background: #2D2D2D;
                border: 2px solid #444;
                border-radius: 6px;
                padding: 8px;
                color: white;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #FF2B43;
            }
            QComboBox {
                background: #2D2D2D;
                border: 2px solid #444;
                border-radius: 6px;
                padding: 8px;
                color: white;
                min-height: 20px;
            }
            QComboBox:focus {
                border-color: #FF2B43;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
            }
            QCheckBox {
                color: white;
                font-size: 12px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 3px;
                border: 2px solid #444;
                background: #2D2D2D;
            }
            QCheckBox::indicator:checked {
                background: #FF2B43;
                border-color: #FF2B43;
            }
            QTabWidget::pane {
                border: 2px solid #444;
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
            QTabBar::tab:hover {
                background: #3D3D3D;
            }
            QTextEdit {
                background: #1E1E1E;
                border: 2px solid #444;
                border-radius: 8px;
                color: white;
            }
            QSpinBox {
                background: #2D2D2D;
                border: 2px solid #444;
                border-radius: 6px;
                padding: 8px;
                color: white;
            }
            QSpinBox:focus {
                border-color: #FF2B43;
            }
        """)

# Функция для интеграции с основным приложением
def show_modern_settings(parent=None):
    """Показать современные настройки"""
    dialog = ModernSettingsDialog(parent)
    return dialog.exec_()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    dialog = ModernSettingsDialog()
    dialog.show()
    sys.exit(app.exec_())
