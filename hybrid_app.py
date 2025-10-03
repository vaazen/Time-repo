# hybrid_app.py - Гибридное приложение с несколькими языками программирования
import sys
import os
import json
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QLabel, QTextEdit, QTabWidget,
                             QLineEdit, QComboBox, QTimeEdit, QDialog, QFormLayout,
                             QDialogButtonBox, QMessageBox, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QTime
from PyQt5.QtGui import QFont

# Попытка импорта WebEngine с fallback
try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    WEBENGINE_AVAILABLE = True
except ImportError:
    print("PyQtWebEngine не доступен, используется упрощенная версия dashboard")
    QWebEngineView = None
    WEBENGINE_AVAILABLE = False

# Импорты наших модулей
from localization_system import localization, _
from task_manager import task_manager, Task, TaskStatus, TaskPriority

# Новые улучшенные модули (с ленивой инициализацией)
from smart_notifications import get_smart_notification_manager, NotificationType
from advanced_analytics import get_advanced_analytics_widget
from enhanced_ui import DragDropTaskWidget, TimelineWidget, ModernTaskDialog
from cloud_sync import cloud_sync_manager, data_exporter
from performance_optimizer import get_performance_optimizer

# Новые модули v5.0
try:
    from ai_assistant import AIAssistant, AIAssistantUI, integrate_ai_assistant
    from integrations_manager import IntegrationsManager, IntegrationsUI, integrate_external_services
    AI_MODULES_AVAILABLE = True
except ImportError as e:
    print(f"ИИ модули недоступны: {e}")
    AI_MODULES_AVAILABLE = False



class JavaScriptUIComponent(QWidget if not WEBENGINE_AVAILABLE else QWebEngineView):
    """UI компонент Dashboard с реальными данными"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        
        if WEBENGINE_AVAILABLE:
            self.setup_webengine_ui()
        else:
            self.setup_native_ui()
        
        # Таймер для обновления данных
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_dashboard_data)
        self.update_timer.start(1000)  # Обновляем каждую секунду
    
    def setup_native_ui(self):
        """Настройка нативного UI без WebEngine"""
        layout = QVBoxLayout()
        
        # Московское время
        self.time_frame = QWidget()
        time_layout = QVBoxLayout(self.time_frame)
        
        self.moscow_time_label = QLabel("Московское время")
        self.moscow_time_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #FF2B43; text-align: center;")
        self.moscow_time_label.setAlignment(Qt.AlignCenter)
        
        self.time_display = QLabel("00:00:00")
        self.time_display.setStyleSheet("font-size: 32px; font-weight: bold; color: #FF2B43; text-align: center;")
        self.time_display.setAlignment(Qt.AlignCenter)
        
        self.date_display = QLabel("Дата")
        self.date_display.setStyleSheet("font-size: 14px; color: #CCCCCC; text-align: center;")
        self.date_display.setAlignment(Qt.AlignCenter)
        
        time_layout.addWidget(self.moscow_time_label)
        time_layout.addWidget(self.time_display)
        time_layout.addWidget(self.date_display)
        
        self.time_frame.setStyleSheet("""
            QWidget {
                background: rgba(255, 43, 67, 0.1);
                border: 2px solid #FF2B43;
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
            }
        """)
        
        layout.addWidget(self.time_frame)
        
        # Статистические карточки
        stats_layout = QHBoxLayout()
        
        # Продуктивность
        self.productivity_card = self.create_stat_card("Продуктивность", "0%", "#FF2B43")
        stats_layout.addWidget(self.productivity_card)
        
        # Время
        self.time_card = self.create_stat_card("Время сегодня", "0:00", "#FFC107")
        stats_layout.addWidget(self.time_card)
        
        # Задачи
        self.tasks_card = self.create_stat_card("Задачи", "0", "#4CAF50")
        stats_layout.addWidget(self.tasks_card)
        
        layout.addLayout(stats_layout)
        
        # Детальная информация
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setMaximumHeight(200)
        self.details_text.setStyleSheet("""
            QTextEdit {
                background: #2D2D2D;
                border: 2px solid #FF2B43;
                border-radius: 8px;
                padding: 10px;
                color: white;
                font-family: 'Consolas', monospace;
            }
        """)
        layout.addWidget(self.details_text)
        
        self.setLayout(layout)
        
        # Стили для всего виджета
        self.setStyleSheet("""
            QWidget {
                background: #1E1E1E;
                color: white;
            }
        """)
    
    def create_stat_card(self, title, value, color):
        """Создание карточки статистики"""
        card = QWidget()
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {color};")
        title_label.setAlignment(Qt.AlignCenter)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        value_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        card.setStyleSheet(f"""
            QWidget {{
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid {color};
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
            }}
        """)
        
        # Сохраняем ссылку на value_label для обновления
        card.value_label = value_label
        
        return card
    
    def setup_webengine_ui(self):
        """Настройка JavaScript UI"""
        html_content = '''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Interactive Dashboard</title>
            <style>
                body {
                    background: linear-gradient(135deg, #1e1e1e, #2d2d2d);
                    color: white;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                }
                .dashboard {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                }
                .card {
                    background: rgba(255, 43, 67, 0.1);
                    border: 2px solid #FF2B43;
                    border-radius: 15px;
                    padding: 20px;
                    transition: transform 0.3s ease;
                }
                .card:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 10px 20px rgba(255, 43, 67, 0.3);
                }
                .card-title {
                    font-size: 18px;
                    font-weight: bold;
                    margin-bottom: 10px;
                    color: #FF2B43;
                }
                .card-value {
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 5px;
                }
                .progress-bar {
                    width: 100%;
                    height: 8px;
                    background: #333;
                    border-radius: 4px;
                    overflow: hidden;
                }
                .progress-fill {
                    height: 100%;
                    background: linear-gradient(90deg, #FF2B43, #FF6B7F);
                    transition: width 0.5s ease;
                }
                .chart-container {
                    width: 100%;
                    height: 200px;
                    margin-top: 15px;
                }
                #productivity-chart {
                    width: 100%;
                    height: 100%;
                }
            </style>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <!-- Московское время -->
            <div class="card" style="grid-column: 1 / -1; text-align: center; margin-bottom: 20px;">
                <div class="card-title" id="moscow-time-title">🕐 Московское время</div>
                <div class="card-value" id="moscow-time" style="font-size: 36px; color: #FF2B43;">00:00:00</div>
                <div id="moscow-date" style="font-size: 16px; color: #CCCCCC; margin-top: 5px;">Дата</div>
            </div>
            
            <div class="dashboard">
                <div class="card">
                    <div class="card-title" id="productivity-title">📊 Продуктивность</div>
                    <div class="card-value" id="productivity-value">0%</div>
                    <div class="progress-bar">
                        <div class="progress-fill" id="productivity-progress" style="width: 0%"></div>
                    </div>
                    <div style="margin-top: 10px; font-size: 12px; color: #CCCCCC;" id="efficiency-text">
                        Эффективность: <span id="efficiency-value">0%</span>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-title" id="time-title">⏰ Время сегодня</div>
                    <div class="card-value" id="time-value">0:00</div>
                    <div class="progress-bar">
                        <div class="progress-fill" id="time-progress" style="width: 0%"></div>
                    </div>
                    <div style="margin-top: 10px; font-size: 12px; color: #CCCCCC;" id="time-details">
                        Запланировано: <span id="planned-time">0</span> мин
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-title" id="tasks-title">📋 Задачи</div>
                    <div class="card-value" id="tasks-value">0</div>
                    <div style="margin-top: 10px;">
                        <span style="color: #4CAF50;" id="completed-label">✓ Выполнено: <span id="completed-tasks">0</span></span><br>
                        <span style="color: #FFC107;" id="pending-label">⏳ В ожидании: <span id="pending-tasks">0</span></span>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-title" id="chart-title">📈 График недели</div>
                    <div class="chart-container">
                        <canvas id="productivity-chart"></canvas>
                    </div>
                </div>
            </div>
            
            <script>
                // Инициализация графика
                const ctx = document.getElementById('productivity-chart').getContext('2d');
                const chart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
                        datasets: [{
                            label: 'Продуктивность %',
                            data: [65, 78, 82, 75, 90, 85, 88],
                            borderColor: '#FF2B43',
                            backgroundColor: 'rgba(255, 43, 67, 0.1)',
                            tension: 0.4,
                            fill: true
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                labels: {
                                    color: 'white'
                                }
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100,
                                ticks: {
                                    color: 'white'
                                },
                                grid: {
                                    color: 'rgba(255, 255, 255, 0.1)'
                                }
                            },
                            x: {
                                ticks: {
                                    color: 'white'
                                },
                                grid: {
                                    color: 'rgba(255, 255, 255, 0.1)'
                                }
                            }
                        }
                    }
                });
                
                // Функция обновления московского времени
                function updateLocalTime() {
                    const now = new Date();
                    // Используем локальное системное время
                    
                    const timeString = now.toLocaleTimeString('ru-RU', {
                        hour: '2-digit',
                        minute: '2-digit', 
                        second: '2-digit'
                    });
                    
                    const dateString = now.toLocaleDateString('ru-RU', {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                    });
                    
                    document.getElementById('moscow-time').textContent = timeString;
                    document.getElementById('moscow-date').textContent = dateString;
                }
                
                // Функция обновления данных dashboard
                function updateDashboard(data) {
                    // Продуктивность
                    document.getElementById('productivity-value').textContent = data.productivity_percent + '%';
                    document.getElementById('productivity-progress').style.width = data.productivity_percent + '%';
                    document.getElementById('efficiency-value').textContent = data.efficiency + '%';
                    
                    // Время
                    const hours = Math.floor(data.total_time_completed / 60);
                    const minutes = data.total_time_completed % 60;
                    document.getElementById('time-value').textContent = hours + ':' + String(minutes).padStart(2, '0');
                    
                    const timeProgress = data.total_time_planned > 0 ? (data.total_time_completed / data.total_time_planned) * 100 : 0;
                    document.getElementById('time-progress').style.width = Math.min(100, timeProgress) + '%';
                    document.getElementById('planned-time').textContent = data.total_time_planned;
                    
                    // Задачи
                    document.getElementById('tasks-value').textContent = data.total_tasks;
                    document.getElementById('completed-tasks').textContent = data.completed_tasks;
                    document.getElementById('pending-tasks').textContent = data.pending_tasks;
                    
                    // Обновляем график недели
                    if (data.weekly_data && data.weekly_data.length > 0) {
                        const labels = data.weekly_data.map(d => d.day_name);
                        const productivity_data = data.weekly_data.map(d => d.productivity);
                        
                        chart.data.labels = labels;
                        chart.data.datasets[0].data = productivity_data;
                        chart.update('none'); // Без анимации для плавности
                    }
                }
                
                // Функция обновления переводов
                function updateTranslations(translations) {
                    document.getElementById('moscow-time-title').innerHTML = '🕐 ' + translations.moscow_time;
                    document.getElementById('productivity-title').innerHTML = '📊 ' + translations.productivity;
                    document.getElementById('time-title').innerHTML = '⏰ ' + translations.time_spent;
                    document.getElementById('tasks-title').innerHTML = '📋 ' + translations.tasks_today;
                    document.getElementById('chart-title').innerHTML = '📈 ' + translations.weekly_stats;
                    document.getElementById('completed-label').innerHTML = '✓ ' + translations.completed_tasks + ': <span id="completed-tasks">0</span>';
                    document.getElementById('pending-label').innerHTML = '⏳ ' + translations.pending_tasks + ': <span id="pending-tasks">0</span>';
                    document.getElementById('efficiency-text').innerHTML = translations.efficiency + ': <span id="efficiency-value">0%</span>';
                    document.getElementById('time-details').innerHTML = 'Запланировано: <span id="planned-time">0</span> мин';
                }
                
                // Обновляем локальное время каждую секунду
                setInterval(updateLocalTime, 1000);
                updateLocalTime(); // Начальное обновление
                
                // Глобальная функция для обновления из Python
                window.updateDashboardData = updateDashboard;
                window.updateDashboardTranslations = updateTranslations;
            </script>
        </body>
        </html>
        '''
        
        self.setHtml(html_content)
    
    def update_dashboard_data(self):
        """Обновление данных dashboard"""
        if not self.parent_app:
            return
            
        # Получаем реальные данные из task_manager
        productivity_data = task_manager.calculate_productivity_today()
        weekly_data = task_manager.get_weekly_stats()
        
        # Обновляем московское время
        moscow_time = localization.get_moscow_time()
        
        if WEBENGINE_AVAILABLE and hasattr(self, 'page'):
            # WebEngine версия
            dashboard_data = {
                'productivity_percent': productivity_data['productivity_percent'],
                'efficiency': productivity_data['efficiency'],
                'total_tasks': productivity_data['total_tasks'],
                'completed_tasks': productivity_data['completed_tasks'],
                'pending_tasks': productivity_data['pending_tasks'],
                'total_time_planned': productivity_data['total_time_planned'],
                'total_time_completed': productivity_data['total_time_completed'],
                'weekly_data': weekly_data
            }
            
            # Отправляем данные в JavaScript
            js_code = f"if (window.updateDashboardData) {{ window.updateDashboardData({json.dumps(dashboard_data)}); }}"
            self.page().runJavaScript(js_code)
        else:
            # Нативная версия
            self.update_native_dashboard(productivity_data, moscow_time)
    
    def update_native_dashboard(self, productivity_data, moscow_time):
        """Обновление нативного dashboard"""
        # Обновляем время
        if hasattr(self, 'time_display'):
            time_str = moscow_time.strftime('%H:%M:%S')
            date_str = moscow_time.strftime('%A, %d %B %Y')
            
            self.time_display.setText(time_str)
            self.date_display.setText(date_str)
        
        # Обновляем карточки статистики
        if hasattr(self, 'productivity_card'):
            self.productivity_card.value_label.setText(f"{productivity_data['productivity_percent']:.1f}%")
        
        if hasattr(self, 'time_card'):
            hours = productivity_data['total_time_completed'] // 60
            minutes = productivity_data['total_time_completed'] % 60
            self.time_card.value_label.setText(f"{hours}:{minutes:02d}")
        
        if hasattr(self, 'tasks_card'):
            self.tasks_card.value_label.setText(str(productivity_data['total_tasks']))
        
        # Обновляем детальную информацию
        if hasattr(self, 'details_text'):
            details = f"""Детальная статистика на {moscow_time.strftime('%d.%m.%Y %H:%M')}:

Задачи:
  • Всего: {productivity_data['total_tasks']}
  • Выполнено: {productivity_data['completed_tasks']}
  • В ожидании: {productivity_data['pending_tasks']}
  • Продуктивность: {productivity_data['productivity_percent']:.1f}%

Время:
  • Запланировано: {productivity_data['total_time_planned']} мин
  • Выполнено: {productivity_data['total_time_completed']} мин
  • Эффективность: {productivity_data['efficiency']:.1f}%

Статус: {'WebEngine недоступен' if not WEBENGINE_AVAILABLE else 'WebEngine активен'}
Обновлено: {moscow_time.strftime('%H:%M:%S')}"""
            
            self.details_text.setPlainText(details)
    
    def update_translations(self):
        """Обновление переводов в dashboard"""
        translations = {
            'moscow_time': _('moscow_time'),
            'productivity': _('productivity'),
            'time_spent': _('time_spent'),
            'tasks_today': _('tasks_today'),
            'weekly_stats': _('weekly_stats'),
            'completed_tasks': _('completed_tasks'),
            'pending_tasks': _('pending_tasks'),
            'efficiency': _('efficiency')
        }
        
        js_code = f"if (window.updateDashboardTranslations) {{ window.updateDashboardTranslations({json.dumps(translations)}); }}"
        self.page().runJavaScript(js_code)

class TaskDialog(QDialog):
    """Диалог для добавления/редактирования задач"""
    
    def __init__(self, parent=None, task=None):
        super().__init__(parent)
        self.task = task
        self.is_edit_mode = task is not None
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка UI диалога"""
        title = _("edit") if self.is_edit_mode else _("add_task")
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QFormLayout()
        
        # Название задачи
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText(_("task_name"))
        layout.addRow(_("task_name") + ":", self.title_edit)
        
        # Описание
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)
        self.description_edit.setPlaceholderText(_("description"))
        layout.addRow(_("description") + ":", self.description_edit)
        
        # Время начала
        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setTime(QTime.currentTime())
        layout.addRow(_("start_time") + ":", self.start_time_edit)
        
        # Время окончания
        self.end_time_edit = QTimeEdit()
        self.end_time_edit.setTime(QTime.currentTime().addSecs(3600))  # +1 час
        layout.addRow(_("end_time") + ":", self.end_time_edit)
        
        # Приоритет
        self.priority_combo = QComboBox()
        self.priority_combo.addItems([
            _("priority_low"),
            _("priority_medium"), 
            _("priority_high"),
            _("priority_urgent")
        ])
        self.priority_combo.setCurrentIndex(1)  # Medium по умолчанию
        layout.addRow(_("priority") + ":", self.priority_combo)
        
        # Статус (только для редактирования)
        if self.is_edit_mode:
            self.status_combo = QComboBox()
            self.status_combo.addItems([
                _("status_planned"),
                _("status_in_progress"),
                _("status_completed"),
                _("status_cancelled")
            ])
            layout.addRow(_("status") + ":", self.status_combo)
        
        # Кнопки
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        # Переводим кнопки
        buttons.button(QDialogButtonBox.Ok).setText(_("save"))
        buttons.button(QDialogButtonBox.Cancel).setText(_("cancel"))
        
        layout.addRow(buttons)
        self.setLayout(layout)
        
        # Заполняем данные при редактировании
        if self.is_edit_mode and self.task:
            self.fill_task_data()
        
        # Стили
        self.setStyleSheet("""
            QDialog {
                background: #1E1E1E;
                color: white;
            }
            QLineEdit, QTextEdit, QTimeEdit, QComboBox {
                background: #2D2D2D;
                border: 2px solid #FF2B43;
                border-radius: 6px;
                padding: 8px;
                color: white;
                font-size: 12px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #FF2B43;
            }
            QPushButton {
                background: #FF2B43;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 120px;
                min-height: 35px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #FF4A5F;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
        """)
    
    def fill_task_data(self):
        """Заполнение данных задачи при редактировании"""
        if not self.task:
            return
            
        self.title_edit.setText(self.task.title)
        self.description_edit.setPlainText(self.task.description)
        
        # Конвертируем datetime в QTime
        start_qtime = QTime(self.task.start_time.hour, self.task.start_time.minute)
        end_qtime = QTime(self.task.end_time.hour, self.task.end_time.minute)
        
        self.start_time_edit.setTime(start_qtime)
        self.end_time_edit.setTime(end_qtime)
        
        # Устанавливаем приоритет
        priority_map = {
            TaskPriority.LOW: 0,
            TaskPriority.MEDIUM: 1,
            TaskPriority.HIGH: 2,
            TaskPriority.URGENT: 3
        }
        self.priority_combo.setCurrentIndex(priority_map.get(self.task.priority, 1))
        
        # Устанавливаем статус (если есть)
        if hasattr(self, 'status_combo'):
            status_map = {
                TaskStatus.PLANNED: 0,
                TaskStatus.IN_PROGRESS: 1,
                TaskStatus.COMPLETED: 2,
                TaskStatus.CANCELLED: 3
            }
            self.status_combo.setCurrentIndex(status_map.get(self.task.status, 0))
    
    def get_task_data(self):
        """Получение данных задачи из формы"""
        # Получаем московское время
        moscow_time = localization.get_moscow_time()
        today = moscow_time.date()
        
        # Создаем datetime объекты для времени
        start_time = datetime.combine(today, self.start_time_edit.time().toPyTime())
        end_time = datetime.combine(today, self.end_time_edit.time().toPyTime())
        
        # Если время окончания меньше времени начала, добавляем день
        if end_time <= start_time:
            end_time = end_time + timedelta(days=1)
        
        # Приоритет
        priority_map = [TaskPriority.LOW, TaskPriority.MEDIUM, TaskPriority.HIGH, TaskPriority.URGENT]
        priority = priority_map[self.priority_combo.currentIndex()]
        
        # Статус (если редактируем)
        status = TaskStatus.PLANNED
        if hasattr(self, 'status_combo'):
            status_map = [TaskStatus.PLANNED, TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED, TaskStatus.CANCELLED]
            status = status_map[self.status_combo.currentIndex()]
        
        return {
            'title': self.title_edit.text().strip(),
            'description': self.description_edit.toPlainText().strip(),
            'start_time': start_time,
            'end_time': end_time,
            'priority': priority,
            'status': status
        }

class HybridTimeBlockingApp(QMainWindow):
    """Главное гибридное приложение"""
    
    def __init__(self):
        super().__init__()
        
        # Модули производительности удалены для упрощения
        
        # Данные приложения
        self.time_blocks = []
        
        # Инициализируем улучшенные модули после создания QApplication
        self.init_enhanced_modules()
        
        self.init_ui()
        self.setup_timers()
    
    def init_enhanced_modules(self):
        """Инициализация улучшенных модулей в правильном потоке"""
        try:
            # Инициализируем менеджеры только если QApplication уже создано
            from PyQt5.QtWidgets import QApplication
            if QApplication.instance() is not None:
                self.smart_notification_manager = get_smart_notification_manager()
                self.advanced_analytics_widget = get_advanced_analytics_widget()
                self.performance_optimizer = get_performance_optimizer()
                
                # Инициализация новых модулей v5.0
                if AI_MODULES_AVAILABLE:
                    self.init_ai_modules()
                
                print("Улучшенные модули успешно инициализированы")
            else:
                print("QApplication не найдено, улучшенные модули будут инициализированы позже")
        except Exception as e:
            print(f"Ошибка инициализации улучшенных модулей: {e}")
            # Устанавливаем заглушки
            self.smart_notification_manager = None
            self.advanced_analytics_widget = None
            self.performance_optimizer = None
    
    def init_ai_modules(self):
        """Инициализация ИИ модулей"""
        try:
            # Создаем ИИ-помощника с ключом OpenAI
            openai_key = "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"
            self.ai_assistant = AIAssistant(openai_key)
            self.ai_ui = AIAssistantUI(self, self.ai_assistant)
            
            # Создаем менеджер интеграций
            self.integrations_manager = IntegrationsManager()
            self.integrations_ui = IntegrationsUI(self, self.integrations_manager)
            
            print("ИИ-помощник и интеграции инициализированы")
        except Exception as e:
            print(f"Ошибка инициализации ИИ модулей: {e}")
            self.ai_assistant = None
            self.ai_ui = None
            self.integrations_manager = None
            self.integrations_ui = None
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle("Hybrid Time Blocking Planner")
        self.setGeometry(100, 100, 1400, 900)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Заголовок
        header = QLabel("Hybrid Time Blocking Planner")
        header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #FF2B43;
            padding: 20px;
            text-align: center;
        """)
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)
        
        # Информация о модулях (упрощено)
        self.modules_info = QLabel("Статус: Python активен | JavaScript активен | Время синхронизировано")
        self.modules_info.setStyleSheet("""
            background: #2D2D2D;
            padding: 10px;
            border-radius: 6px;
            font-family: 'Consolas', monospace;
            color: #CCCCCC;
        """)
        main_layout.addWidget(self.modules_info)
        
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
        
        # Вкладка JavaScript Dashboard
        self.js_dashboard = JavaScriptUIComponent(self)
        self.tabs.addTab(self.js_dashboard, _("tab_dashboard"))
        
        # Вкладка управления задачами
        self.tasks_tab = self.create_tasks_tab()
        self.tabs.addTab(self.tasks_tab, _("tab_tasks"))
        
        # Новые вкладки v5.0
        if AI_MODULES_AVAILABLE and hasattr(self, 'ai_ui') and self.ai_ui:
            self.ai_tab = self.create_ai_tab()
            self.tabs.addTab(self.ai_tab, "🤖 ИИ-Помощник")
            
            self.integrations_tab = self.create_integrations_tab()
            self.tabs.addTab(self.integrations_tab, "🔗 Интеграции")
        
        # Добавляем вкладку настроек
        self.settings_tab = self.create_settings_tab()
        self.tabs.addTab(self.settings_tab, "⚙️ Настройки")
        
        # Вкладка производительности удалена для упрощения
        
        main_layout.addWidget(self.tabs)
        
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
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 120px;
                min-height: 35px;
            }
            QPushButton:hover {
                background: #FF4A5F;
            }
            QTextEdit {
                background: #2D2D2D;
                border: 2px solid #FF2B43;
                border-radius: 6px;
                padding: 10px;
                font-family: 'Consolas', monospace;
            }
            QLabel {
                margin: 5px;
            }
        """)
    
    def create_tasks_tab(self):
        """Создание вкладки управления задачами"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Заголовок и кнопки управления
        header_layout = QHBoxLayout()
        
        # Переключатель языков
        lang_layout = QHBoxLayout()
        lang_label = QLabel(_("language") + ":")
        self.language_combo = QComboBox()
        
        for code, name in localization.get_supported_languages().items():
            self.language_combo.addItem(name, code)
        
        # Устанавливаем текущий язык
        current_lang = localization.current_language
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == current_lang:
                self.language_combo.setCurrentIndex(i)
                break
        
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.language_combo)
        lang_layout.addStretch()
        
        header_layout.addLayout(lang_layout)
        
        # Кнопки управления задачами
        buttons_layout = QHBoxLayout()
        
        add_task_btn = QPushButton(_("add_task"))
        add_task_btn.clicked.connect(self.add_task_dialog)
        
        refresh_btn = QPushButton("Обновить")
        refresh_btn.clicked.connect(self.refresh_tasks)
        
        buttons_layout.addWidget(add_task_btn)
        buttons_layout.addWidget(refresh_btn)
        buttons_layout.addStretch()
        
        header_layout.addLayout(buttons_layout)
        layout.addLayout(header_layout)
        
        # Список задач
        self.tasks_list = QListWidget()
        self.tasks_list.setStyleSheet("""
            QListWidget {
                background: #2D2D2D;
                border: 2px solid #FF2B43;
                border-radius: 8px;
                padding: 10px;
            }
            QListWidget::item {
                background: #1E1E1E;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 10px;
                margin: 5px;
                color: white;
            }
            QListWidget::item:selected {
                background: #FF2B43;
            }
            QListWidget::item:hover {
                background: #3D3D3D;
            }
        """)
        
        layout.addWidget(self.tasks_list)
        
        # Кнопки действий с задачами
        task_actions_layout = QHBoxLayout()
        
        edit_btn = QPushButton(_("edit"))
        edit_btn.clicked.connect(self.edit_selected_task)
        
        complete_btn = QPushButton(_("complete"))
        complete_btn.clicked.connect(self.complete_selected_task)
        
        delete_btn = QPushButton(_("delete"))
        delete_btn.clicked.connect(self.delete_selected_task)
        
        task_actions_layout.addWidget(edit_btn)
        task_actions_layout.addWidget(complete_btn)
        task_actions_layout.addWidget(delete_btn)
        task_actions_layout.addStretch()
        
        layout.addLayout(task_actions_layout)
        
        widget.setLayout(layout)
        
        # Загружаем задачи
        self.refresh_tasks()
        
        return widget
    
    def create_blocks_tab(self):
        """Создание вкладки управления блоками"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("+ Добавить блок")
        add_btn.clicked.connect(self.add_time_block)
        
        process_btn = QPushButton("Обработать (Rust)")
        process_btn.clicked.connect(self.process_with_rust)
        
        calculate_btn = QPushButton("Рассчитать (C++)")
        calculate_btn.clicked.connect(self.calculate_with_cpp)
        
        buttons_layout.addWidget(add_btn)
        buttons_layout.addWidget(process_btn)
        buttons_layout.addWidget(calculate_btn)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        # Область для отображения результатов
        self.results_area = QTextEdit()
        self.results_area.setPlainText("Добро пожаловать в гибридное приложение!\n\nИспользуются языки:\n• Python - основа и UI\n• C++ - вычисления производительности\n• Rust - обработка данных\n• JavaScript - интерактивная панель\n\nДобавьте временные блоки и протестируйте функциональность!")
        layout.addWidget(self.results_area)
        
        # Информация о модулях
        self.modules_info = QLabel(info_text)
        self.modules_info.setText(info_text)
        self.modules_info.setStyleSheet("""
            background: #2D2D2D;
            padding: 10px;
            border-radius: 6px;
            font-family: 'Consolas', monospace;
            color: #CCCCCC;
        """)
    
    def setup_timers(self):
        """Настройка таймеров"""
        # Таймер для обновления статистики
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_statistics)
        self.stats_timer.start(5000)  # Каждые 5 секунд
    
    def add_time_block(self):
        """Добавление временного блока"""
        import random
        
        # Генерируем случайный блок для демонстрации
        block = {
            'id': len(self.time_blocks) + 1,
            'title': f'Задача {len(self.time_blocks) + 1}',
            'duration': random.randint(30, 180),  # 30-180 минут
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        self.time_blocks.append(block)
        
        self.results_area.append(f"\n+ Добавлен блок: {block['title']} ({block['duration']} мин)")
        self.results_area.append(f"   Всего блоков: {len(self.time_blocks)}")
    
    def process_with_rust(self):
        """Обработка данных с помощью Rust"""
        if not self.time_blocks:
            self.results_area.append("\nНет блоков для обработки")
            return
        
        self.results_area.append(f"\nОбработка {len(self.time_blocks)} блоков с помощью Rust...")
        
        # Обработка через Rust модуль
        result = self.rust_processor.process_time_blocks(self.time_blocks)
        
        processor = result.get('processor', 'unknown')
        efficiency = result.get('total_efficiency', 0)
        
        self.results_area.append(f"Обработка завершена ({processor})")
        self.results_area.append(f"Общая эффективность: {efficiency:.1f}%")
    
    def calculate_with_cpp(self):
        """Расчет производительности с помощью C++"""
        if not self.time_blocks:
            self.results_area.append("\nНет блоков для расчета")
            return
        
        self.results_area.append(f"\nРасчет производительности для {len(self.time_blocks)} блоков...")
        
        # Простой расчет продуктивности на Python
        if not self.time_blocks:
            productivity = 0.0
        else:
            total_minutes = sum(block.get('duration', 0) for block in self.time_blocks)
            # 8 часов = 100% продуктивности
            productivity = min(100.0, (total_minutes / 480.0) * 100.0)
        
        self.results_area.append(f"Расчет завершен (Python)")
        self.results_area.append(f"Продуктивность: {productivity:.1f}%")
    
    
    def update_statistics(self):
        """Обновление статистики"""
        if self.time_blocks:
            total_duration = sum(block['duration'] for block in self.time_blocks)
            avg_duration = total_duration / len(self.time_blocks)
            
            # Обновляем заголовок окна со статистикой
            self.setWindowTitle(f"Hybrid App - Блоков: {len(self.time_blocks)}, Время: {total_duration} мин")
    
    def on_language_changed(self):
        """Обработка смены языка"""
        selected_code = self.language_combo.currentData()
        if selected_code and localization.set_language(selected_code):
            # Обновляем заголовок окна
            self.setWindowTitle(_("app_title"))
            
            # Обновляем переводы в dashboard
            if hasattr(self, 'js_dashboard'):
                self.js_dashboard.update_translations()
            
            # Обновляем список задач
            self.refresh_tasks()
            
            # Показываем сообщение
            QMessageBox.information(self, _("language"), _("language_changed", localization.get_supported_languages()[selected_code]))
    
    def add_task_dialog(self):
        """Диалог добавления новой задачи"""
        dialog = TaskDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            task_data = dialog.get_task_data()
            
            if not task_data['title']:
                QMessageBox.warning(self, _("add_task"), "Введите название задачи")
                return
            
            # Создаем задачу
            task = task_manager.create_task(
                title=task_data['title'],
                description=task_data['description'],
                start_time=task_data['start_time'],
                end_time=task_data['end_time'],
                priority=task_data['priority']
            )
            
            # Обновляем список
            self.refresh_tasks()
            
            # Показываем сообщение
            QMessageBox.information(self, _("add_task"), _("task_added"))
    
    def edit_selected_task(self):
        """Редактирование выбранной задачи"""
        current_item = self.tasks_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, _("edit"), "Выберите задачу для редактирования")
            return
        
        task_id = current_item.data(Qt.UserRole)
        task = task_manager.get_task_by_id(task_id)
        
        if not task:
            QMessageBox.warning(self, _("edit"), "Задача не найдена")
            return
        
        dialog = TaskDialog(self, task)
        if dialog.exec_() == QDialog.Accepted:
            task_data = dialog.get_task_data()
            
            if not task_data['title']:
                QMessageBox.warning(self, _("edit"), "Введите название задачи")
                return
            
            # Обновляем задачу
            task_manager.update_task(
                task_id,
                title=task_data['title'],
                description=task_data['description'],
                start_time=task_data['start_time'],
                end_time=task_data['end_time'],
                priority=task_data['priority'],
                status=task_data['status']
            )
            
            # Обновляем список
            self.refresh_tasks()
            
            QMessageBox.information(self, _("edit"), "Задача обновлена")
    
    def complete_selected_task(self):
        """Завершение выбранной задачи"""
        current_item = self.tasks_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, _("complete"), "Выберите задачу для завершения")
            return
        
        task_id = current_item.data(Qt.UserRole)
        task = task_manager.complete_task(task_id)
        
        if task:
            self.refresh_tasks()
            QMessageBox.information(self, _("complete"), _("task_completed"))
        else:
            QMessageBox.warning(self, _("complete"), "Не удалось завершить задачу")
    
    def delete_selected_task(self):
        """Удаление выбранной задачи"""
        current_item = self.tasks_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, _("delete"), "Выберите задачу для удаления")
            return
        
        task_id = current_item.data(Qt.UserRole)
        task = task_manager.get_task_by_id(task_id)
        
        if not task:
            QMessageBox.warning(self, _("delete"), "Задача не найдена")
            return
        
        # Подтверждение удаления
        reply = QMessageBox.question(
            self, _("delete"), 
            f"Удалить задачу '{task.title}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if task_manager.delete_task(task_id):
                self.refresh_tasks()
                QMessageBox.information(self, _("delete"), _("task_deleted"))
            else:
                QMessageBox.warning(self, _("delete"), "Не удалось удалить задачу")
    
    def refresh_tasks(self):
        """Обновление списка задач"""
        self.tasks_list.clear()
        
        today_tasks = task_manager.get_tasks_for_today()
        
        if not today_tasks:
            item = QListWidgetItem(_("no_tasks"))
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
            self.tasks_list.addItem(item)
            return
        
        # Сортируем задачи по времени начала
        today_tasks.sort(key=lambda t: t.start_time)
        
        for task in today_tasks:
            # Формируем текст элемента
            status_text = self.get_status_text(task.status)
            priority_text = self.get_priority_text(task.priority)
            time_text = f"{task.start_time.strftime('%H:%M')} - {task.end_time.strftime('%H:%M')}"
            
            # Определяем цвет статуса
            status_color = self.get_status_color(task.status)
            
            item_text = f"[{status_text}] {task.title}\n"
            item_text += f"⏰ {time_text} | 🎯 {priority_text}\n"
            
            if task.description:
                item_text += f"📝 {task.description[:50]}{'...' if len(task.description) > 50 else ''}"
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, task.id)
            
            # Устанавливаем цвет в зависимости от статуса
            item.setBackground(status_color)
            
            self.tasks_list.addItem(item)
    
    def get_status_text(self, status: TaskStatus) -> str:
        """Получение текста статуса на текущем языке"""
        status_map = {
            TaskStatus.PLANNED: _("status_planned"),
            TaskStatus.IN_PROGRESS: _("status_in_progress"),
            TaskStatus.COMPLETED: _("status_completed"),
            TaskStatus.CANCELLED: _("status_cancelled")
        }
        return status_map.get(status, str(status.value))
    
    def get_priority_text(self, priority: TaskPriority) -> str:
        """Получение текста приоритета на текущем языке"""
        priority_map = {
            TaskPriority.LOW: _("priority_low"),
            TaskPriority.MEDIUM: _("priority_medium"),
            TaskPriority.HIGH: _("priority_high"),
            TaskPriority.URGENT: _("priority_urgent")
        }
        return priority_map.get(priority, str(priority.value))
    
    def get_status_color(self, status: TaskStatus):
        """Получение цвета для статуса задачи"""
        from PyQt5.QtGui import QColor
        
        color_map = {
            TaskStatus.PLANNED: QColor(70, 70, 70),      # Серый
            TaskStatus.IN_PROGRESS: QColor(255, 193, 7), # Желтый
            TaskStatus.COMPLETED: QColor(76, 175, 80),   # Зеленый
            TaskStatus.CANCELLED: QColor(244, 67, 54)    # Красный
        }
        return color_map.get(status, QColor(70, 70, 70))
    
    def create_ai_tab(self):
        """Создание вкладки ИИ-помощника"""
        ai_widget = QWidget()
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("🤖 ИИ-Помощник для планирования")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Кнопки функций
        buttons_layout = QHBoxLayout()
        
        analyze_btn = QPushButton("📊 Анализ задач")
        analyze_btn.clicked.connect(self.analyze_tasks_with_ai)
        buttons_layout.addWidget(analyze_btn)
        
        schedule_btn = QPushButton("⏰ Умное планирование")
        schedule_btn.clicked.connect(self.smart_scheduling)
        buttons_layout.addWidget(schedule_btn)
        
        insights_btn = QPushButton("💡 Инсайты")
        insights_btn.clicked.connect(self.show_productivity_insights)
        buttons_layout.addWidget(insights_btn)
        
        chat_btn = QPushButton("💬 Чат с ИИ")
        chat_btn.clicked.connect(self.open_ai_chat)
        buttons_layout.addWidget(chat_btn)
        
        reset_btn = QPushButton("🔄 Сброс API")
        reset_btn.clicked.connect(self.reset_ai_api)
        buttons_layout.addWidget(reset_btn)
        
        layout.addLayout(buttons_layout)
        
        # Область результатов
        self.ai_results = QTextEdit()
        self.ai_results.setPlaceholderText("Результаты анализа ИИ будут отображаться здесь...")
        layout.addWidget(self.ai_results)
        
        ai_widget.setLayout(layout)
        return ai_widget
    
    def create_integrations_tab(self):
        """Создание вкладки интеграций"""
        integrations_widget = QWidget()
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("🔗 Интеграции с внешними сервисами")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Slack секция
        slack_group = QWidget()
        slack_layout = QVBoxLayout()
        slack_title = QLabel("📱 Slack")
        slack_title.setStyleSheet("font-size: 14px; font-weight: bold;")
        slack_layout.addWidget(slack_title)
        
        slack_buttons = QHBoxLayout()
        setup_slack_btn = QPushButton("Настроить Slack")
        setup_slack_btn.clicked.connect(self.setup_slack_integration)
        test_slack_btn = QPushButton("Тест уведомления")
        test_slack_btn.clicked.connect(self.test_slack_notification)
        
        slack_buttons.addWidget(setup_slack_btn)
        slack_buttons.addWidget(test_slack_btn)
        slack_layout.addLayout(slack_buttons)
        slack_group.setLayout(slack_layout)
        layout.addWidget(slack_group)
        
        # Trello секция
        trello_group = QWidget()
        trello_layout = QVBoxLayout()
        trello_title = QLabel("📋 Trello")
        trello_title.setStyleSheet("font-size: 14px; font-weight: bold;")
        trello_layout.addWidget(trello_title)
        
        trello_buttons = QHBoxLayout()
        setup_trello_btn = QPushButton("Настроить Trello")
        setup_trello_btn.clicked.connect(self.setup_trello_integration)
        sync_trello_btn = QPushButton("Синхронизировать")
        sync_trello_btn.clicked.connect(self.sync_with_trello)
        
        trello_buttons.addWidget(setup_trello_btn)
        trello_buttons.addWidget(sync_trello_btn)
        trello_layout.addLayout(trello_buttons)
        trello_group.setLayout(trello_layout)
        layout.addWidget(trello_group)
        
        # Notion секция
        notion_group = QWidget()
        notion_layout = QVBoxLayout()
        notion_title = QLabel("📝 Notion")
        notion_title.setStyleSheet("font-size: 14px; font-weight: bold;")
        notion_layout.addWidget(notion_title)
        
        notion_buttons = QHBoxLayout()
        setup_notion_btn = QPushButton("Настроить Notion")
        setup_notion_btn.clicked.connect(self.setup_notion_integration)
        sync_notion_btn = QPushButton("Синхронизировать")
        sync_notion_btn.clicked.connect(self.sync_with_notion)
        
        notion_buttons.addWidget(setup_notion_btn)
        notion_buttons.addWidget(sync_notion_btn)
        notion_layout.addLayout(notion_buttons)
        notion_group.setLayout(notion_layout)
        layout.addWidget(notion_group)
        
        # Статус интеграций
        self.integrations_status = QTextEdit()
        self.integrations_status.setPlaceholderText("Статус интеграций будет отображаться здесь...")
        self.update_integrations_status()
        layout.addWidget(self.integrations_status)
        
        integrations_widget.setLayout(layout)
        return integrations_widget
    
    # Методы для ИИ-помощника
    def analyze_tasks_with_ai(self):
        """Анализ задач с помощью ИИ"""
        if not hasattr(self, 'ai_assistant') or not self.ai_assistant:
            QMessageBox.warning(self, "Ошибка", "ИИ-помощник недоступен")
            return
        
        self.ai_results.setText("🔄 Анализирую ваши задачи...")
        
        # Получаем задачи из task_manager
        tasks = task_manager.get_all_tasks()
        if not tasks:
            self.ai_results.setText("❌ Нет задач для анализа")
            return
        
        # Конвертируем задачи в формат для ИИ
        tasks_data = []
        for task in tasks:
            task_dict = {
                "title": task.title,
                "description": task.description,
                "priority": task.priority.value,
                "status": task.status.value,
                "created_at": task.created_at.isoformat() if hasattr(task, 'created_at') else "",
                "deadline": task.end_time.isoformat() if task.end_time else ""
            }
            tasks_data.append(task_dict)
        
        # Запускаем анализ в отдельном потоке
        import threading
        def analyze():
            try:
                analysis = self.ai_assistant.analyze_tasks(tasks_data)
                result_text = "🤖 Анализ ваших задач:\n\n"
                
                for key, value in analysis.items():
                    result_text += f"📋 {key.upper()}:\n"
                    if isinstance(value, list):
                        for item in value:
                            result_text += f"  • {item}\n"
                    else:
                        result_text += f"  {value}\n"
                    result_text += "\n"
                
                self.ai_results.setText(result_text)
            except Exception as e:
                self.ai_results.setText(f"❌ Ошибка анализа: {str(e)}")
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def smart_scheduling(self):
        """Умное планирование с ИИ"""
        if not hasattr(self, 'ai_assistant') or not self.ai_assistant:
            QMessageBox.warning(self, "Ошибка", "ИИ-помощник недоступен")
            return
        
        self.ai_results.setText("🔄 Создаю оптимальное расписание...")
        
        tasks = task_manager.get_all_tasks()
        if not tasks:
            self.ai_results.setText("❌ Нет задач для планирования")
            return
        
        tasks_data = [{"title": t.title, "description": t.description, "priority": t.priority.value} for t in tasks]
        
        import threading
        def schedule():
            try:
                schedule_data = self.ai_assistant.suggest_time_blocks(tasks_data)
                result_text = "⏰ Рекомендуемое расписание:\n\n"
                
                for block in schedule_data:
                    result_text += f"🕐 {block.get('время_начала', 'N/A')} - {block.get('задача', 'N/A')}\n"
                    result_text += f"   Продолжительность: {block.get('продолжительность', 'N/A')} мин\n"
                    result_text += f"   💡 {block.get('обоснование', '')}\n\n"
                
                self.ai_results.setText(result_text)
            except Exception as e:
                self.ai_results.setText(f"❌ Ошибка планирования: {str(e)}")
        
        threading.Thread(target=schedule, daemon=True).start()
    
    def show_productivity_insights(self):
        """Показать инсайты продуктивности"""
        if not hasattr(self, 'ai_assistant') or not self.ai_assistant:
            QMessageBox.warning(self, "Ошибка", "ИИ-помощник недоступен")
            return
        
        self.ai_results.setText("🔄 Анализирую вашу продуктивность...")
        
        import threading
        def get_insights():
            try:
                all_tasks = task_manager.get_all_tasks()
                completed_tasks = [t for t in all_tasks if t.status == TaskStatus.COMPLETED]
                
                productivity_data = {
                    "total_tasks": len(all_tasks),
                    "completed_tasks": len(completed_tasks),
                    "completion_rate": len(completed_tasks) / max(len(all_tasks), 1) * 100
                }
                
                completed_data = [{"title": t.title, "completion_time": t.end_time.isoformat() if t.end_time else ""} for t in completed_tasks]
                
                insights = self.ai_assistant.productivity_insights(completed_data, productivity_data)
                
                result_text = "📊 Анализ продуктивности:\n\n"
                for key, value in insights.items():
                    result_text += f"📈 {key.upper().replace('_', ' ')}:\n"
                    if isinstance(value, list):
                        for item in value:
                            result_text += f"  • {item}\n"
                    else:
                        result_text += f"  {value}\n"
                    result_text += "\n"
                
                self.ai_results.setText(result_text)
            except Exception as e:
                self.ai_results.setText(f"❌ Ошибка анализа: {str(e)}")
        
        threading.Thread(target=get_insights, daemon=True).start()
    
    def open_ai_chat(self):
        """Открыть чат с ИИ"""
        if not hasattr(self, 'ai_assistant') or not self.ai_assistant:
            QMessageBox.warning(self, "Ошибка", "ИИ-помощник недоступен")
            return
        
        # Создаем простой диалог чата
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit
        
        chat_dialog = QDialog(self)
        chat_dialog.setWindowTitle("💬 Чат с ИИ-помощником")
        chat_dialog.setGeometry(200, 200, 600, 500)
        
        layout = QVBoxLayout()
        
        chat_area = QTextEdit()
        chat_area.setReadOnly(True)
        chat_area.append("🤖 ИИ-Помощник: Привет! Задавайте любые вопросы о планировании и продуктивности!")
        layout.addWidget(chat_area)
        
        input_layout = QHBoxLayout()
        message_input = QLineEdit()
        message_input.setPlaceholderText("Введите ваше сообщение...")
        send_button = QPushButton("Отправить")
        
        def send_message():
            message = message_input.text().strip()
            if not message:
                return
            
            chat_area.append(f"👤 Вы: {message}")
            message_input.clear()
            
            def get_response():
                try:
                    context = {"total_tasks": len(task_manager.get_all_tasks())}
                    response = self.ai_assistant.chat_with_assistant(message, context)
                    chat_area.append(f"🤖 ИИ-Помощник: {response}")
                except Exception as e:
                    chat_area.append(f"🤖 ИИ-Помощник: Извините, произошла ошибка: {str(e)}")
            
            import threading
            threading.Thread(target=get_response, daemon=True).start()
        
        send_button.clicked.connect(send_message)
        message_input.returnPressed.connect(send_message)
        
        input_layout.addWidget(message_input)
        input_layout.addWidget(send_button)
        layout.addLayout(input_layout)
        
        chat_dialog.setLayout(layout)
        chat_dialog.exec_()
    
    def reset_ai_api(self):
        """Сброс статуса API для повторной попытки подключения"""
        if hasattr(self, 'ai_assistant') and self.ai_assistant:
            self.ai_assistant.reset_api_status()
            self.ai_results.setText("🔄 API статус сброшен. Попробуйте использовать ИИ-функции снова.")
            QMessageBox.information(self, "Сброс API", "Статус API сброшен. Теперь система попробует переподключиться к OpenAI.")
        else:
            QMessageBox.warning(self, "Ошибка", "ИИ-помощник недоступен")
    
    # Методы для интеграций
    def setup_slack_integration(self):
        """Настройка интеграции со Slack"""
        if not hasattr(self, 'integrations_manager'):
            QMessageBox.warning(self, "Ошибка", "Менеджер интеграций недоступен")
            return
        
        from PyQt5.QtWidgets import QInputDialog
        
        webhook_url, ok = QInputDialog.getText(self, "Настройка Slack", "Введите Webhook URL:")
        if ok and webhook_url:
            self.integrations_manager.setup_slack(webhook_url=webhook_url)
            QMessageBox.information(self, "Успех", "Slack интеграция настроена!")
            self.update_integrations_status()
    
    def setup_trello_integration(self):
        """Настройка интеграции с Trello"""
        if not hasattr(self, 'integrations_manager'):
            QMessageBox.warning(self, "Ошибка", "Менеджер интеграций недоступен")
            return
        
        from PyQt5.QtWidgets import QInputDialog
        
        api_key, ok1 = QInputDialog.getText(self, "Настройка Trello", "Введите API Key:")
        if not ok1 or not api_key:
            return
        
        token, ok2 = QInputDialog.getText(self, "Настройка Trello", "Введите Token:")
        if ok2 and token:
            self.integrations_manager.setup_trello(api_key, token)
            QMessageBox.information(self, "Успех", "Trello интеграция настроена!")
            self.update_integrations_status()
    
    def setup_notion_integration(self):
        """Настройка интеграции с Notion"""
        if not hasattr(self, 'integrations_manager'):
            QMessageBox.warning(self, "Ошибка", "Менеджер интеграций недоступен")
            return
        
        from PyQt5.QtWidgets import QInputDialog
        
        token, ok = QInputDialog.getText(self, "Настройка Notion", "Введите Integration Token:")
        if ok and token:
            self.integrations_manager.setup_notion(token)
            QMessageBox.information(self, "Успех", "Notion интеграция настроена!")
            self.update_integrations_status()
    
    def test_slack_notification(self):
        """Тест уведомления Slack"""
        if not hasattr(self, 'integrations_manager') or not self.integrations_manager.slack:
            QMessageBox.warning(self, "Ошибка", "Slack не настроен")
            return
        
        test_task = {
            "title": "Тестовая задача",
            "description": "Тест интеграции со Slack",
            "priority": "high"
        }
        
        success = self.integrations_manager.slack.send_task_notification(test_task)
        if success:
            QMessageBox.information(self, "Успех", "Тестовое уведомление отправлено!")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось отправить уведомление")
    
    def sync_with_trello(self):
        """Синхронизация с Trello"""
        QMessageBox.information(self, "Информация", "Функция синхронизации с Trello в разработке")
    
    def sync_with_notion(self):
        """Синхронизация с Notion"""
        QMessageBox.information(self, "Информация", "Функция синхронизации с Notion в разработке")
    
    def update_integrations_status(self):
        """Обновление статуса интеграций"""
        if not hasattr(self, 'integrations_status'):
            return
        
        status_text = "📊 Статус интеграций:\n\n"
        
        if hasattr(self, 'integrations_manager'):
            if self.integrations_manager.slack:
                status_text += "✅ Slack: Настроен\n"
            else:
                status_text += "❌ Slack: Не настроен\n"
            
            if self.integrations_manager.trello:
                status_text += "✅ Trello: Настроен\n"
            else:
                status_text += "❌ Trello: Не настроен\n"
            
            if self.integrations_manager.notion:
                status_text += "✅ Notion: Настроен\n"
            else:
                status_text += "❌ Notion: Не настроен\n"
        else:
            status_text += "❌ Менеджер интеграций недоступен\n"
        
        self.integrations_status.setText(status_text)
    
    def create_settings_tab(self):
        """Создание вкладки настроек"""
        settings_widget = QWidget()
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("⚙️ Настройки приложения")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Кнопка открытия настроек
        open_settings_btn = QPushButton("🔧 Открыть настройки")
        open_settings_btn.clicked.connect(self.open_modern_settings)
        open_settings_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 15px 30px;
                margin: 20px;
                min-height: 50px;
            }
        """)
        layout.addWidget(open_settings_btn)
        
        # Информация о настройках
        info_text = QLabel("""
        <div style='padding: 20px; line-height: 1.6;'>
            <h3>🌟 Доступные настройки:</h3>
            <ul>
                <li><b>🌐 Общие:</b> Язык интерфейса, тема оформления</li>
                <li><b>🤖 ИИ-Помощник:</b> API ключи, модели, поведение</li>
                <li><b>🔗 Интеграции:</b> Slack, Trello, Notion</li>
                <li><b>ℹ️ О программе:</b> Информация о команде разработчиков</li>
            </ul>
            
            <p><i>Настройки автоматически сохраняются и применяются при перезапуске приложения.</i></p>
        </div>
        """)
        info_text.setWordWrap(True)
        info_text.setStyleSheet("color: #CCCCCC; background: #2D2D2D; border-radius: 8px; padding: 15px;")
        layout.addWidget(info_text)
        
        layout.addStretch()
        
        settings_widget.setLayout(layout)
        return settings_widget
    
    def open_modern_settings(self):
        """Открыть современные настройки"""
        try:
            from modern_settings import ModernSettingsDialog
            dialog = ModernSettingsDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                QMessageBox.information(self, "Настройки", "Настройки сохранены! Некоторые изменения требуют перезапуска приложения.")
        except ImportError:
            QMessageBox.warning(self, "Ошибка", "Модуль настроек не найден!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть настройки: {str(e)}")

def main():
    """Главная функция с инициализацией всех улучшений"""
    app = QApplication(sys.argv)
    
    # Безопасный вывод для Windows консоли
    try:
        print("🚀 Запуск революционного приложения Time Blocking v5.0...")
        print("✅ Умные уведомления: активированы")
        print("✅ Продвинутая аналитика: загружена")
        print("✅ Drag & Drop интерфейс: готов")
        print("✅ Облачная синхронизация: настроена")
        print("✅ Оптимизация производительности: включена")
    except UnicodeEncodeError:
        print("Запуск революционного приложения Time Blocking v5.0...")
        print("Умные уведомления: активированы")
        print("Продвинутая аналитика: загружена")
        print("Drag & Drop интерфейс: готов")
        print("Облачная синхронизация: настроена")
        print("Оптимизация производительности: включена")
    
    if AI_MODULES_AVAILABLE:
        try:
            print("🤖 ИИ-помощник: активирован (OpenAI)")
            print("🔗 Интеграции: Slack, Trello, Notion готовы")
        except UnicodeEncodeError:
            print("ИИ-помощник: активирован (OpenAI)")
            print("Интеграции: Slack, Trello, Notion готовы")
    else:
        print("ИИ модули недоступны")
    
    # Создаем и показываем приложение
    window = HybridTimeBlockingApp()
    window.show()
    
    try:
        print("🎉 Приложение успешно запущено!")
        print("📊 Функции v4.0:")
    except UnicodeEncodeError:
        print("Приложение успешно запущено!")
        print("Функции v4.0:")
    
    print("   - Тепловая карта продуктивности")
    print("   - Адаптивные уведомления")
    print("   - Персональные инсайты")
    print("   - Экспорт данных")
    print("   - Улучшенный UI с анимациями")
    
    if AI_MODULES_AVAILABLE:
        try:
            print("🆕 Новые функции v5.0:")
            print("   - 🤖 ИИ-помощник для планирования")
            print("   - 📊 Анализ задач с помощью ИИ")
            print("   - ⏰ Умное планирование расписания")
            print("   - 💬 Чат с ИИ-консультантом")
            print("   - 🔗 Интеграция со Slack")
            print("   - 📋 Интеграция с Trello")
            print("   - 📝 Интеграция с Notion")
        except UnicodeEncodeError:
            print("Новые функции v5.0:")
            print("   - ИИ-помощник для планирования")
            print("   - Анализ задач с помощью ИИ")
            print("   - Умное планирование расписания")
            print("   - Чат с ИИ-консультантом")
            print("   - Интеграция со Slack")
            print("   - Интеграция с Trello")
            print("   - Интеграция с Notion")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
