# test_localization.py - Тест системы локализации
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QLabel, QComboBox
from localization_system import localization, _
from modern_settings import ModernSettings

class LocalizationTestDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.settings = ModernSettings()
        self.setWindowTitle("Тест локализации")
        self.setFixedSize(400, 300)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Заголовок
        self.title_label = QLabel(_("app_title"))
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(self.title_label)
        
        # Выбор языка
        lang_label = QLabel("Выберите язык / Choose language:")
        layout.addWidget(lang_label)
        
        self.language_combo = QComboBox()
        languages = [
            ("🇷🇺 Русский", "ru"),
            ("🇺🇸 English", "en"), 
            ("🇩🇪 Deutsch", "de"),
            ("🇫🇷 Français", "fr"),
            ("🇪🇸 Español", "es")
        ]
        
        for name, code in languages:
            self.language_combo.addItem(name, code)
        
        # Устанавливаем текущий язык
        current_lang = localization.current_language
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == current_lang:
                self.language_combo.setCurrentIndex(i)
                break
        
        self.language_combo.currentIndexChanged.connect(self.change_language)
        layout.addWidget(self.language_combo)
        
        # Тестовые элементы
        self.test_elements = []
        
        self.add_task_btn = QPushButton(_("add_task"))
        self.test_elements.append(("add_task", self.add_task_btn))
        layout.addWidget(self.add_task_btn)
        
        self.dashboard_label = QLabel(_("dashboard"))
        self.test_elements.append(("dashboard", self.dashboard_label))
        layout.addWidget(self.dashboard_label)
        
        self.tasks_label = QLabel(_("tab_tasks"))
        self.test_elements.append(("tab_tasks", self.tasks_label))
        layout.addWidget(self.tasks_label)
        
        self.settings_label = QLabel(_("settings"))
        self.test_elements.append(("settings", self.settings_label))
        layout.addWidget(self.settings_label)
        
        # Кнопка закрытия
        close_btn = QPushButton("Закрыть / Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        # Применяем стили
        self.setStyleSheet("""
            QDialog {
                background: #1E1E1E;
                color: white;
            }
            QPushButton {
                background: #FF2B43;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                margin: 2px;
            }
            QPushButton:hover {
                background: #FF4A5F;
            }
            QLabel {
                color: white;
                margin: 5px;
            }
            QComboBox {
                background: #2D2D2D;
                color: white;
                border: 1px solid #444;
                padding: 5px;
                border-radius: 4px;
            }
        """)
    
    def change_language(self):
        """Изменение языка"""
        selected_lang = self.language_combo.currentData()
        if selected_lang:
            # Применяем новый язык
            localization.set_language(selected_lang)
            
            # Обновляем все элементы интерфейса
            self.update_interface()
    
    def update_interface(self):
        """Обновление интерфейса с новым языком"""
        # Обновляем заголовок
        self.title_label.setText(_("app_title"))
        
        # Обновляем тестовые элементы
        for key, element in self.test_elements:
            if hasattr(element, 'setText'):
                element.setText(_(key))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    print("Тест системы локализации")
    print(f"Текущий язык: {localization.current_language}")
    print(f"Поддерживаемые языки: {list(localization.supported_languages.keys())}")
    
    # Тестируем переводы
    print("\nТестирование переводов:")
    for lang in ["ru", "en", "de"]:
        localization.set_language(lang)
        print(f"{lang}: {_('app_title')} | {_('add_task')} | {_('dashboard')}")
    
    # Возвращаем русский язык
    localization.set_language("ru")
    
    # Показываем диалог
    dialog = LocalizationTestDialog()
    dialog.show()
    
    sys.exit(app.exec_())
