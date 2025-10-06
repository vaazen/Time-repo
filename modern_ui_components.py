"""
🎨 Современные UI компоненты с улучшенным дизайном
Обеспечивает красивый и отзывчивый пользовательский интерфейс
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from typing import Optional, List, Dict, Any

class ModernButton(QPushButton):
    """Современная кнопка с анимацией и градиентами"""
    
    def __init__(self, text: str = "", icon: Optional[QIcon] = None, 
                 color: str = "#FF2B43", parent=None):
        super().__init__(text, parent)
        self.base_color = color
        self.hover_color = self._lighten_color(color, 20)
        self.pressed_color = self._darken_color(color, 20)
        
        if icon:
            self.setIcon(icon)
            self.setIconSize(QSize(20, 20))
        
        self.setMinimumHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        self._setup_style()
        self._setup_animations()
    
    def _setup_style(self):
        """Настройка стилей"""
        self.setStyleSheet(f"""
            ModernButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.base_color}, stop:1 {self._darken_color(self.base_color, 10)});
                border: none;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 8px 16px;
            }}
            ModernButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.hover_color}, stop:1 {self._darken_color(self.hover_color, 10)});
            }}
            ModernButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.pressed_color}, stop:1 {self._darken_color(self.pressed_color, 10)});
            }}
        """)
    
    def _setup_animations(self):
        """Настройка анимаций"""
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(150)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
    
    def _lighten_color(self, color: str, amount: int) -> str:
        """Осветление цвета"""
        color = QColor(color)
        h, s, l, a = color.getHsl()
        l = min(255, l + amount)
        color.setHsl(h, s, l, a)
        return color.name()
    
    def _darken_color(self, color: str, amount: int) -> str:
        """Затемнение цвета"""
        color = QColor(color)
        h, s, l, a = color.getHsl()
        l = max(0, l - amount)
        color.setHsl(h, s, l, a)
        return color.name()

class ModernCard(QFrame):
    """Современная карточка с тенью и скругленными углами"""
    
    def __init__(self, title: str = "", content_widget: Optional[QWidget] = None, 
                 parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.NoFrame)
        self._setup_ui(title, content_widget)
        self._setup_style()
    
    def _setup_ui(self, title: str, content_widget: Optional[QWidget]):
        """Настройка интерфейса"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    font-weight: bold;
                    color: #333333;
                    margin-bottom: 10px;
                }
            """)
            layout.addWidget(title_label)
        
        if content_widget:
            layout.addWidget(content_widget)
    
    def _setup_style(self):
        """Настройка стилей"""
        self.setStyleSheet("""
            ModernCard {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 12px;
            }
        """)
        
        # Добавляем тень
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

class ModernProgressBar(QProgressBar):
    """Современный прогресс-бар с анимацией"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(8)
        self.setMaximumHeight(8)
        self._setup_style()
        self._setup_animation()
    
    def _setup_style(self):
        """Настройка стилей"""
        self.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: #F0F0F0;
                text-align: center;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF2B43, stop:1 #FF6B43);
                border-radius: 4px;
            }
        """)
    
    def _setup_animation(self):
        """Настройка анимации"""
        self.animation = QPropertyAnimation(self, b"value")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
    
    def setValueAnimated(self, value: int):
        """Установка значения с анимацией"""
        self.animation.setStartValue(self.value())
        self.animation.setEndValue(value)
        self.animation.start()

class ModernTaskItem(QWidget):
    """Современный элемент задачи"""
    
    task_clicked = pyqtSignal(str)  # ID задачи
    task_completed = pyqtSignal(str)  # ID задачи
    
    def __init__(self, task_data: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.task_data = task_data
        self.is_completed = task_data.get('status') == 'completed'
        self._setup_ui()
        self._setup_style()
    
    def _setup_ui(self):
        """Настройка интерфейса"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)
        
        # Чекбокс для завершения
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(self.is_completed)
        self.checkbox.toggled.connect(self._on_checkbox_toggled)
        layout.addWidget(self.checkbox)
        
        # Основная информация
        info_layout = QVBoxLayout()
        
        # Заголовок задачи
        self.title_label = QLabel(self.task_data.get('title', 'Без названия'))
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
            }
        """)
        info_layout.addWidget(self.title_label)
        
        # Описание и метаданные
        meta_text = []
        if 'priority' in self.task_data:
            meta_text.append(f"Приоритет: {self.task_data['priority']}")
        if 'duration' in self.task_data:
            meta_text.append(f"Время: {self.task_data['duration']} мин")
        
        if meta_text:
            self.meta_label = QLabel(" • ".join(meta_text))
            self.meta_label.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    color: #666666;
                }
            """)
            info_layout.addWidget(self.meta_label)
        
        layout.addLayout(info_layout, 1)
        
        # Прогресс-бар (если есть прогресс)
        if 'progress' in self.task_data:
            self.progress_bar = ModernProgressBar()
            self.progress_bar.setValue(self.task_data['progress'])
            layout.addWidget(self.progress_bar)
        
        # Кнопка действий
        self.action_btn = ModernButton("⋯", color="#666666")
        self.action_btn.setMaximumWidth(40)
        self.action_btn.clicked.connect(self._on_action_clicked)
        layout.addWidget(self.action_btn)
        
        self._update_completion_style()
    
    def _setup_style(self):
        """Настройка стилей"""
        self.setStyleSheet("""
            ModernTaskItem {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                margin: 2px;
            }
            ModernTaskItem:hover {
                background-color: #F8F9FA;
                border-color: #FF2B43;
            }
        """)
        
        self.setCursor(Qt.PointingHandCursor)
    
    def _on_checkbox_toggled(self, checked: bool):
        """Обработка изменения чекбокса"""
        self.is_completed = checked
        self._update_completion_style()
        self.task_completed.emit(self.task_data.get('id', ''))
    
    def _on_action_clicked(self):
        """Обработка клика по кнопке действий"""
        self.task_clicked.emit(self.task_data.get('id', ''))
    
    def _update_completion_style(self):
        """Обновление стиля в зависимости от завершенности"""
        if self.is_completed:
            self.title_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: bold;
                    color: #999999;
                    text-decoration: line-through;
                }
            """)
        else:
            self.title_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: bold;
                    color: #333333;
                }
            """)
    
    def mousePressEvent(self, event):
        """Обработка клика по элементу"""
        if event.button() == Qt.LeftButton:
            self.task_clicked.emit(self.task_data.get('id', ''))
        super().mousePressEvent(event)

class ModernSearchBox(QLineEdit):
    """Современное поле поиска"""
    
    def __init__(self, placeholder: str = "Поиск...", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self._setup_style()
        self._setup_search_icon()
    
    def _setup_style(self):
        """Настройка стилей"""
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0;
                border-radius: 20px;
                padding: 8px 40px 8px 15px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #FF2B43;
                outline: none;
            }
        """)
        self.setMinimumHeight(40)
    
    def _setup_search_icon(self):
        """Добавление иконки поиска"""
        search_action = QAction(self)
        search_action.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        self.addAction(search_action, QLineEdit.TrailingPosition)

class ModernTabWidget(QTabWidget):
    """Современный виджет вкладок"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_style()
    
    def _setup_style(self):
        """Настройка стилей"""
        self.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                background-color: white;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background-color: #F8F9FA;
                border: 1px solid #E0E0E0;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 12px 20px;
                margin-right: 2px;
                font-weight: bold;
                color: #666666;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #FF2B43;
                border-bottom: 2px solid #FF2B43;
            }
            QTabBar::tab:hover:!selected {
                background-color: #F0F0F0;
                color: #333333;
            }
        """)

class ModernSidebar(QWidget):
    """Современная боковая панель"""
    
    item_clicked = pyqtSignal(str)  # Название элемента
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.items = []
        self.selected_item = None
        self._setup_ui()
        self._setup_style()
    
    def _setup_ui(self):
        """Настройка интерфейса"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 20, 0, 20)
        self.layout.setSpacing(5)
        
        # Заголовок
        title_label = QLabel("Навигация")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                padding: 10px 20px;
            }
        """)
        self.layout.addWidget(title_label)
        
        # Разделитель
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("QFrame { color: #E0E0E0; }")
        self.layout.addWidget(separator)
        
        self.layout.addStretch()
    
    def _setup_style(self):
        """Настройка стилей"""
        self.setStyleSheet("""
            ModernSidebar {
                background-color: #F8F9FA;
                border-right: 1px solid #E0E0E0;
            }
        """)
        self.setFixedWidth(250)
    
    def add_item(self, name: str, icon: Optional[QIcon] = None):
        """Добавление элемента в боковую панель"""
        item_btn = QPushButton(name)
        if icon:
            item_btn.setIcon(icon)
        
        item_btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 12px 20px;
                border: none;
                background-color: transparent;
                font-size: 14px;
                color: #666666;
            }
            QPushButton:hover {
                background-color: #E9ECEF;
                color: #333333;
            }
            QPushButton:checked {
                background-color: #FF2B43;
                color: white;
                font-weight: bold;
            }
        """)
        
        item_btn.setCheckable(True)
        item_btn.clicked.connect(lambda: self._on_item_clicked(name))
        
        # Вставляем перед stretch
        self.layout.insertWidget(self.layout.count() - 1, item_btn)
        self.items.append((name, item_btn))
    
    def _on_item_clicked(self, name: str):
        """Обработка клика по элементу"""
        # Снимаем выделение с других элементов
        for item_name, btn in self.items:
            btn.setChecked(item_name == name)
        
        self.selected_item = name
        self.item_clicked.emit(name)
    
    def select_item(self, name: str):
        """Программное выделение элемента"""
        self._on_item_clicked(name)

class ModernStatusBar(QStatusBar):
    """Современная строка состояния"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_style()
        self._setup_widgets()
    
    def _setup_style(self):
        """Настройка стилей"""
        self.setStyleSheet("""
            QStatusBar {
                background-color: #F8F9FA;
                border-top: 1px solid #E0E0E0;
                color: #666666;
                font-size: 12px;
            }
        """)
    
    def _setup_widgets(self):
        """Настройка виджетов"""
        # Индикатор статуса
        self.status_label = QLabel("Готов")
        self.addWidget(self.status_label)
        
        # Прогресс-бар для длительных операций
        self.progress_bar = ModernProgressBar()
        self.progress_bar.setVisible(False)
        self.addPermanentWidget(self.progress_bar)
        
        # Информация о времени
        self.time_label = QLabel()
        self.addPermanentWidget(self.time_label)
        
        # Таймер для обновления времени
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_time)
        self.timer.start(1000)
        self._update_time()
    
    def _update_time(self):
        """Обновление времени"""
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.setText(current_time)
    
    def show_progress(self, message: str = "Обработка..."):
        """Показать прогресс"""
        self.status_label.setText(message)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Неопределенный прогресс
    
    def hide_progress(self):
        """Скрыть прогресс"""
        self.status_label.setText("Готов")
        self.progress_bar.setVisible(False)
    
    def set_progress(self, value: int, maximum: int = 100):
        """Установить значение прогресса"""
        self.progress_bar.setRange(0, maximum)
        self.progress_bar.setValueAnimated(value)
