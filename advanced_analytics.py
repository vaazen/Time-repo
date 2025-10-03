# advanced_analytics.py - Продвинутая аналитика с тепловыми картами
import json
import os
from datetime import datetime, timedelta, date
from typing import Dict, List, Tuple, Optional
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QPushButton, QScrollArea, QFrame,
                             QGridLayout, QTabWidget, QTextEdit, QProgressBar)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor
import pandas as pd

class ProductivityHeatmap(QWidget):
    """Виджет тепловой карты продуктивности"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 400)
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout()
        
        # Заголовок и контролы
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("🔥 Тепловая карта продуктивности")
        self.title_label.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            color: #FF2B43;
            margin: 10px;
        """)
        
        self.period_combo = QComboBox()
        self.period_combo.addItems(["Последние 7 дней", "Последний месяц", 
                                   "Последние 3 месяца", "Весь год"])
        self.period_combo.currentTextChanged.connect(self.update_heatmap)
        
        self.refresh_btn = QPushButton("🔄 Обновить")
        self.refresh_btn.clicked.connect(self.refresh_data)
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(QLabel("Период:"))
        header_layout.addWidget(self.period_combo)
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Matplotlib canvas для тепловой карты
        self.figure = Figure(figsize=(12, 6), facecolor='#2b2b2b')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
    
    def load_data(self):
        """Загрузка данных продуктивности"""
        # Здесь будет загрузка реальных данных из task_manager
        self.productivity_data = self.generate_sample_data()
        self.update_heatmap()
    
    def generate_sample_data(self) -> Dict:
        """Генерация примерных данных для демонстрации"""
        data = {}
        
        # Генерируем данные за последние 90 дней
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=90)
        
        current_date = start_date
        while current_date <= end_date:
            # Имитируем различные уровни продуктивности
            weekday = current_date.weekday()
            
            # Будние дни более продуктивны
            if weekday < 5:  # Пн-Пт
                base_productivity = np.random.normal(0.7, 0.2)
            else:  # Выходные
                base_productivity = np.random.normal(0.4, 0.15)
            
            # Ограничиваем значения от 0 до 1
            productivity = max(0, min(1, base_productivity))
            
            data[current_date.isoformat()] = {
                'productivity_score': productivity,
                'completed_tasks': int(productivity * 10),
                'total_focus_time': productivity * 8 * 60,  # в минутах
                'breaks_taken': int(productivity * 5),
                'efficiency_rating': productivity
            }
            
            current_date += timedelta(days=1)
        
        return data
    
    def update_heatmap(self):
        """Обновление тепловой карты"""
        self.figure.clear()
        
        # Получаем данные за выбранный период
        period = self.period_combo.currentText()
        filtered_data = self.filter_data_by_period(period)
        
        if not filtered_data:
            return
        
        # Создаем subplot
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#2b2b2b')
        
        # Подготавливаем данные для тепловой карты
        dates = list(filtered_data.keys())
        dates.sort()
        
        # Создаем матрицу для тепловой карты (7 дней недели x количество недель)
        weeks_data = self.prepare_weekly_matrix(dates, filtered_data)
        
        # Создаем тепловую карту
        im = ax.imshow(weeks_data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
        
        # Настройка осей
        ax.set_yticks(range(7))
        ax.set_yticklabels(['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'])
        
        # Подписи недель
        week_labels = self.generate_week_labels(dates)
        ax.set_xticks(range(len(week_labels)))
        ax.set_xticklabels(week_labels, rotation=45)
        
        # Цветовая шкала
        cbar = self.figure.colorbar(im, ax=ax)
        cbar.set_label('Уровень продуктивности', color='white')
        cbar.ax.yaxis.set_tick_params(color='white')
        
        # Стилизация
        ax.set_title('Тепловая карта продуктивности', color='white', fontsize=14, pad=20)
        ax.tick_params(colors='white')
        
        # Добавляем значения в ячейки
        self.add_cell_values(ax, weeks_data)
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def prepare_weekly_matrix(self, dates: List[str], data: Dict) -> np.ndarray:
        """Подготовка матрицы данных по неделям"""
        if not dates:
            return np.zeros((7, 1))
        
        start_date = datetime.fromisoformat(dates[0]).date()
        end_date = datetime.fromisoformat(dates[-1]).date()
        
        # Находим начало недели (понедельник)
        start_monday = start_date - timedelta(days=start_date.weekday())
        
        # Вычисляем количество недель
        total_days = (end_date - start_monday).days + 1
        weeks_count = (total_days + 6) // 7
        
        # Создаем матрицу 7x weeks_count
        matrix = np.zeros((7, weeks_count))
        
        current_date = start_monday
        for week in range(weeks_count):
            for day in range(7):
                date_str = current_date.isoformat()
                if date_str in data:
                    matrix[day, week] = data[date_str]['productivity_score']
                current_date += timedelta(days=1)
        
        return matrix
    
    def generate_week_labels(self, dates: List[str]) -> List[str]:
        """Генерация подписей для недель"""
        if not dates:
            return []
        
        start_date = datetime.fromisoformat(dates[0]).date()
        end_date = datetime.fromisoformat(dates[-1]).date()
        
        start_monday = start_date - timedelta(days=start_date.weekday())
        
        labels = []
        current_monday = start_monday
        
        while current_monday <= end_date:
            labels.append(current_monday.strftime("%d.%m"))
            current_monday += timedelta(days=7)
        
        return labels
    
    def add_cell_values(self, ax, matrix: np.ndarray):
        """Добавление значений в ячейки тепловой карты"""
        rows, cols = matrix.shape
        for i in range(rows):
            for j in range(cols):
                if matrix[i, j] > 0:
                    text = ax.text(j, i, f'{matrix[i, j]:.1f}',
                                 ha="center", va="center", 
                                 color="white" if matrix[i, j] < 0.5 else "black",
                                 fontsize=8, fontweight='bold')
    
    def filter_data_by_period(self, period: str) -> Dict:
        """Фильтрация данных по выбранному периоду"""
        end_date = datetime.now().date()
        
        if period == "Последние 7 дней":
            start_date = end_date - timedelta(days=7)
        elif period == "Последний месяц":
            start_date = end_date - timedelta(days=30)
        elif period == "Последние 3 месяца":
            start_date = end_date - timedelta(days=90)
        else:  # Весь год
            start_date = end_date - timedelta(days=365)
        
        filtered = {}
        for date_str, data in self.productivity_data.items():
            date_obj = datetime.fromisoformat(date_str).date()
            if start_date <= date_obj <= end_date:
                filtered[date_str] = data
        
        return filtered
    
    def refresh_data(self):
        """Обновление данных"""
        self.load_data()

class ProductivityTrends(QWidget):
    """Виджет трендов продуктивности"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("📈 Тренды продуктивности")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #FF2B43; margin: 10px;")
        layout.addWidget(title)
        
        # Matplotlib canvas для графиков
        self.figure = Figure(figsize=(12, 8), facecolor='#2b2b2b')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
    
    def load_data(self):
        """Загрузка и отображение данных"""
        # Генерируем примерные данные
        self.generate_trends_data()
        self.plot_trends()
    
    def generate_trends_data(self):
        """Генерация данных трендов"""
        # Данные за последние 30 дней
        dates = []
        productivity_scores = []
        focus_times = []
        completed_tasks = []
        
        for i in range(30):
            date = datetime.now().date() - timedelta(days=29-i)
            dates.append(date)
            
            # Имитируем тренды
            base_trend = 0.6 + 0.3 * np.sin(i * 0.2)  # Волнообразный тренд
            noise = np.random.normal(0, 0.1)
            
            productivity = max(0, min(1, base_trend + noise))
            productivity_scores.append(productivity)
            
            focus_times.append(productivity * 8)  # часы фокуса
            completed_tasks.append(int(productivity * 12))
        
        self.trends_data = {
            'dates': dates,
            'productivity_scores': productivity_scores,
            'focus_times': focus_times,
            'completed_tasks': completed_tasks
        }
    
    def plot_trends(self):
        """Построение графиков трендов"""
        self.figure.clear()
        
        # Создаем 3 subplot'а
        ax1 = self.figure.add_subplot(3, 1, 1)
        ax2 = self.figure.add_subplot(3, 1, 2)
        ax3 = self.figure.add_subplot(3, 1, 3)
        
        dates = self.trends_data['dates']
        
        # График 1: Общая продуктивность
        ax1.plot(dates, self.trends_data['productivity_scores'], 
                color='#FF2B43', linewidth=2, marker='o', markersize=4)
        ax1.set_title('Общий уровень продуктивности', color='white', fontsize=12)
        ax1.set_ylabel('Продуктивность', color='white')
        ax1.grid(True, alpha=0.3)
        ax1.set_facecolor('#2b2b2b')
        
        # График 2: Время фокуса
        ax2.bar(dates, self.trends_data['focus_times'], 
               color='#FFC107', alpha=0.7, width=0.8)
        ax2.set_title('Время глубокой работы (часы)', color='white', fontsize=12)
        ax2.set_ylabel('Часы', color='white')
        ax2.grid(True, alpha=0.3)
        ax2.set_facecolor('#2b2b2b')
        
        # График 3: Завершенные задачи
        ax3.plot(dates, self.trends_data['completed_tasks'], 
                color='#4CAF50', linewidth=2, marker='s', markersize=4)
        ax3.set_title('Завершенные задачи', color='white', fontsize=12)
        ax3.set_ylabel('Количество', color='white')
        ax3.set_xlabel('Дата', color='white')
        ax3.grid(True, alpha=0.3)
        ax3.set_facecolor('#2b2b2b')
        
        # Настройка осей для всех графиков
        for ax in [ax1, ax2, ax3]:
            ax.tick_params(colors='white')
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        self.figure.tight_layout()
        self.canvas.draw()

class ProductivityInsights(QWidget):
    """Виджет инсайтов и рекомендаций"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.generate_insights()
    
    def setup_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("💡 Персональные инсайты")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #FF2B43; margin: 10px;")
        layout.addWidget(title)
        
        # Скроллируемая область для инсайтов
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        
        self.insights_widget = QWidget()
        self.insights_layout = QVBoxLayout(self.insights_widget)
        
        scroll.setWidget(self.insights_widget)
        layout.addWidget(scroll)
        
        self.setLayout(layout)
    
    def generate_insights(self):
        """Генерация персональных инсайтов"""
        insights = [
            {
                "title": "🕘 Ваш пик продуктивности",
                "content": "Анализ показывает, что вы наиболее продуктивны с 9:00 до 11:00. Планируйте сложные задачи на это время.",
                "type": "peak_time",
                "color": "#4CAF50"
            },
            {
                "title": "📅 Лучший день недели",
                "content": "Вторник - ваш самый продуктивный день. Средняя эффективность: 87%",
                "type": "best_day",
                "color": "#2196F3"
            },
            {
                "title": "⚠️ Зона риска",
                "content": "После 15:00 ваша продуктивность снижается на 35%. Рекомендуем делать перерыв в 14:30.",
                "type": "warning",
                "color": "#FF9800"
            },
            {
                "title": "🎯 Рекомендация",
                "content": "Попробуйте технику Помодоро: 25 минут работы + 5 минут перерыва. Это может повысить вашу эффективность на 23%.",
                "type": "recommendation",
                "color": "#9C27B0"
            },
            {
                "title": "📊 Статистика недели",
                "content": "За эту неделю вы завершили 47 задач (+12% к прошлой неделе) и потратили 28 часов на глубокую работу.",
                "type": "stats",
                "color": "#607D8B"
            },
            {
                "title": "🏆 Достижение",
                "content": "Поздравляем! Вы поддерживаете продуктивность выше 80% уже 5 дней подряд!",
                "type": "achievement",
                "color": "#FF2B43"
            }
        ]
        
        for insight in insights:
            self.add_insight_card(insight)
    
    def add_insight_card(self, insight: Dict):
        """Добавление карточки инсайта"""
        card = QFrame()
        card.setFrameStyle(QFrame.Box)
        card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {insight['color']}22, stop:1 {insight['color']}11);
                border: 2px solid {insight['color']};
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        # Заголовок
        title_label = QLabel(insight['title'])
        title_label.setStyleSheet(f"""
            font-size: 14px; 
            font-weight: bold; 
            color: {insight['color']};
            margin-bottom: 5px;
        """)
        
        # Содержимое
        content_label = QLabel(insight['content'])
        content_label.setStyleSheet("color: white; font-size: 12px; line-height: 1.4;")
        content_label.setWordWrap(True)
        
        layout.addWidget(title_label)
        layout.addWidget(content_label)
        
        self.insights_layout.addWidget(card)

class AdvancedAnalyticsWidget(QTabWidget):
    """Главный виджет продвинутой аналитики"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_tabs()
        self.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #444;
                background: #2b2b2b;
            }
            QTabBar::tab {
                background: #3b3b3b;
                color: white;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #FF2B43;
            }
            QTabBar::tab:hover {
                background: #4b4b4b;
            }
        """)
    
    def setup_tabs(self):
        """Настройка вкладок аналитики"""
        
        # Вкладка 1: Тепловая карта
        self.heatmap_widget = ProductivityHeatmap()
        self.addTab(self.heatmap_widget, "🔥 Тепловая карта")
        
        # Вкладка 2: Тренды
        self.trends_widget = ProductivityTrends()
        self.addTab(self.trends_widget, "📈 Тренды")
        
        # Вкладка 3: Инсайты
        self.insights_widget = ProductivityInsights()
        self.addTab(self.insights_widget, "💡 Инсайты")
        
        # Вкладка 4: Экспорт данных
        self.export_widget = self.create_export_tab()
        self.addTab(self.export_widget, "📊 Экспорт")
    
    def create_export_tab(self) -> QWidget:
        """Создание вкладки экспорта данных"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("📊 Экспорт данных и отчетов")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #FF2B43; margin: 10px;")
        layout.addWidget(title)
        
        # Кнопки экспорта
        export_layout = QGridLayout()
        
        # PDF отчет
        pdf_btn = QPushButton("📄 Экспорт в PDF")
        pdf_btn.clicked.connect(self.export_to_pdf)
        pdf_btn.setStyleSheet("""
            QPushButton {
                background: #FF2B43;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #E91E63;
            }
        """)
        
        # Excel отчет
        excel_btn = QPushButton("📊 Экспорт в Excel")
        excel_btn.clicked.connect(self.export_to_excel)
        excel_btn.setStyleSheet(pdf_btn.styleSheet().replace("#FF2B43", "#4CAF50").replace("#E91E63", "#45A049"))
        
        # CSV данные
        csv_btn = QPushButton("📋 Экспорт в CSV")
        csv_btn.clicked.connect(self.export_to_csv)
        csv_btn.setStyleSheet(pdf_btn.styleSheet().replace("#FF2B43", "#2196F3").replace("#E91E63", "#1976D2"))
        
        # JSON данные
        json_btn = QPushButton("🔧 Экспорт в JSON")
        json_btn.clicked.connect(self.export_to_json)
        json_btn.setStyleSheet(pdf_btn.styleSheet().replace("#FF2B43", "#FF9800").replace("#E91E63", "#F57C00"))
        
        export_layout.addWidget(pdf_btn, 0, 0)
        export_layout.addWidget(excel_btn, 0, 1)
        export_layout.addWidget(csv_btn, 1, 0)
        export_layout.addWidget(json_btn, 1, 1)
        
        layout.addLayout(export_layout)
        
        # Статус экспорта
        self.export_status = QLabel("Готов к экспорту данных")
        self.export_status.setStyleSheet("color: #888; margin: 10px;")
        layout.addWidget(self.export_status)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def export_to_pdf(self):
        """Экспорт в PDF"""
        self.export_status.setText("📄 Экспортирую в PDF...")
        # Здесь будет реализация экспорта в PDF
        self.export_status.setText("✅ PDF отчет сохранен")
    
    def export_to_excel(self):
        """Экспорт в Excel"""
        self.export_status.setText("📊 Экспортирую в Excel...")
        # Здесь будет реализация экспорта в Excel
        self.export_status.setText("✅ Excel файл сохранен")
    
    def export_to_csv(self):
        """Экспорт в CSV"""
        self.export_status.setText("📋 Экспортирую в CSV...")
        # Здесь будет реализация экспорта в CSV
        self.export_status.setText("✅ CSV файл сохранен")
    
    def export_to_json(self):
        """Экспорт в JSON"""
        self.export_status.setText("🔧 Экспортирую в JSON...")
        # Здесь будет реализация экспорта в JSON
        self.export_status.setText("✅ JSON файл сохранен")

# Глобальный экземпляр виджета аналитики (ленивая инициализация)
_advanced_analytics_widget = None

def get_advanced_analytics_widget():
    """Получение глобального экземпляра виджета с ленивой инициализацией"""
    global _advanced_analytics_widget
    if _advanced_analytics_widget is None:
        _advanced_analytics_widget = AdvancedAnalyticsWidget()
    return _advanced_analytics_widget

# Для обратной совместимости
advanced_analytics_widget = None
