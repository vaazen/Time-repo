# enhanced_ui.py - Улучшенный UI с Drag & Drop
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class DragDropTaskWidget(QWidget):
    """Виджет задачи с поддержкой Drag & Drop"""
    
    task_moved = pyqtSignal(str, int, int)  # task_id, new_hour, new_minute
    
    def __init__(self, task_data, parent=None):
        super().__init__(parent)
        self.task_data = task_data
        self.setAcceptDrops(True)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout()
        
        # Иконка приоритета
        priority_icon = QLabel("🔥" if self.task_data.get('priority') == 'high' else "📋")
        
        # Название задачи
        title_label = QLabel(self.task_data.get('title', 'Задача'))
        title_label.setStyleSheet("font-weight: bold; color: white;")
        
        # Время
        time_label = QLabel(f"{self.task_data.get('start_time', '00:00')}")
        time_label.setStyleSheet("color: #888;")
        
        layout.addWidget(priority_icon)
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(time_label)
        
        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF2B43, stop:1 #FF6B7F);
                border-radius: 8px;
                padding: 10px;
                margin: 2px;
            }
            QWidget:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF4B63, stop:1 #FF8B9F);
            }
        """)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
            
    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
            
        if ((event.pos() - self.drag_start_position).manhattanLength() < 
            QApplication.startDragDistance()):
            return
            
        # Начинаем drag операцию
        drag = QDrag(self)
        mimeData = QMimeData()
        mimeData.setText(self.task_data.get('id', ''))
        drag.setMimeData(mimeData)
        
        # Создаем pixmap для перетаскивания
        pixmap = self.grab()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        
        dropAction = drag.exec_(Qt.MoveAction)

class TimelineWidget(QScrollArea):
    """Временная шкала с поддержкой Drag & Drop"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setup_timeline()
        
    def setup_timeline(self):
        """Настройка временной шкалы"""
        self.timeline_widget = QWidget()
        self.timeline_layout = QVBoxLayout(self.timeline_widget)
        
        # Создаем слоты времени (24 часа)
        self.time_slots = {}
        for hour in range(24):
            hour_widget = self.create_hour_slot(hour)
            self.timeline_layout.addWidget(hour_widget)
            self.time_slots[hour] = hour_widget
            
        self.setWidget(self.timeline_widget)
        self.setWidgetResizable(True)
        
    def create_hour_slot(self, hour):
        """Создание слота для часа"""
        slot_widget = QFrame()
        slot_widget.setFrameStyle(QFrame.Box)
        slot_widget.setMinimumHeight(60)
        slot_widget.setAcceptDrops(True)
        
        layout = QHBoxLayout(slot_widget)
        
        # Время
        time_label = QLabel(f"{hour:02d}:00")
        time_label.setStyleSheet("font-weight: bold; color: #FF2B43; min-width: 50px;")
        layout.addWidget(time_label)
        
        # Область для задач
        tasks_area = QWidget()
        tasks_area.setStyleSheet("background: rgba(255, 255, 255, 0.05); border-radius: 5px;")
        layout.addWidget(tasks_area)
        
        slot_widget.hour = hour
        return slot_widget
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        task_id = event.mimeData().text()
        # Определяем час по позиции drop
        pos = event.pos()
        # Здесь логика определения времени по позиции
        print(f"Task {task_id} dropped at position {pos}")
        event.accept()

class ModernTaskDialog(QDialog):
    """Современный диалог создания/редактирования задач"""
    
    def __init__(self, task_data=None, parent=None):
        super().__init__(parent)
        self.task_data = task_data or {}
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("✨ Создание задачи")
        self.setFixedSize(500, 600)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2b2b2b, stop:1 #1a1a1a);
            }
        """)
        
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("🎯 Новая задача")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #FF2B43; margin: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Форма
        form_layout = QFormLayout()
        
        # Название задачи
        self.title_input = QLineEdit()
        self.title_input.setStyleSheet(self.get_input_style())
        self.title_input.setPlaceholderText("Введите название задачи...")
        
        # Описание
        self.description_input = QTextEdit()
        self.description_input.setStyleSheet(self.get_input_style())
        self.description_input.setPlaceholderText("Описание задачи (необязательно)...")
        self.description_input.setMaximumHeight(100)
        
        # Приоритет
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["🔥 Высокий", "📋 Средний", "📝 Низкий"])
        self.priority_combo.setStyleSheet(self.get_input_style())
        
        # Время начала
        self.start_time = QTimeEdit()
        self.start_time.setTime(QTime.currentTime())
        self.start_time.setStyleSheet(self.get_input_style())
        
        # Длительность
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(15, 480)
        self.duration_spin.setValue(60)
        self.duration_spin.setSuffix(" мин")
        self.duration_spin.setStyleSheet(self.get_input_style())
        
        form_layout.addRow("📝 Название:", self.title_input)
        form_layout.addRow("📄 Описание:", self.description_input)
        form_layout.addRow("⚡ Приоритет:", self.priority_combo)
        form_layout.addRow("🕐 Время начала:", self.start_time)
        form_layout.addRow("⏱️ Длительность:", self.duration_spin)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Сохранить")
        save_btn.setStyleSheet("""
            QPushButton {
                background: #FF2B43;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #E91E63;
            }
        """)
        save_btn.clicked.connect(self.accept)
        
        cancel_btn = QPushButton("❌ Отмена")
        cancel_btn.setStyleSheet(save_btn.styleSheet().replace("#FF2B43", "#666").replace("#E91E63", "#777"))
        cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
        self.setLayout(layout)
        
    def get_input_style(self):
        return """
            QLineEdit, QTextEdit, QComboBox, QTimeEdit, QSpinBox {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 43, 67, 0.3);
                border-radius: 6px;
                padding: 8px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QTimeEdit:focus, QSpinBox:focus {
                border-color: #FF2B43;
            }
        """
