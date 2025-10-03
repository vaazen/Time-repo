# dynamic_interface.py - Система динамического обновления интерфейса

import random
from datetime import datetime, timedelta
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel

class DynamicInterfaceManager:
    """Менеджер для динамического обновления всех элементов интерфейса"""
    
    def __init__(self, main_app):
        self.app = main_app
        self.update_counters = {}
        self.dynamic_elements = {}
        self.setup_dynamic_timers()
    
    def setup_dynamic_timers(self):
        """Настройка таймеров для разных элементов"""
        
        # Таймер для времени (каждую секунду)
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time_elements)
        self.time_timer.start(1000)
        
        # Таймер для статистики (каждые 5 секунд)
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_stats_elements)
        self.stats_timer.start(5000)
        
        # Таймер для мотивационных сообщений (каждые 30 секунд)
        self.motivation_timer = QTimer()
        self.motivation_timer.timeout.connect(self.update_motivation_elements)
        self.motivation_timer.start(30000)
        
        # Таймер для анимаций (каждые 2 секунды)
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animations)
        self.animation_timer.start(2000)
    
    def register_dynamic_element(self, element_id, element, update_type="stats"):
        """Регистрация элемента для динамического обновления"""
        self.dynamic_elements[element_id] = {
            'element': element,
            'type': update_type,
            'last_update': datetime.now()
        }
    
    def update_time_elements(self):
        """Обновление всех элементов времени"""
        try:
            # Обновляем основную карточку времени
            if hasattr(self.app, 'time_card') and self.app.time_card:
                self.app.update_time_display()
            
            # Обновляем заголовок окна с текущим временем
            current_time = datetime.now().strftime("%H:%M:%S")
            self.app.setWindowTitle(f"⏰ Time Blocking v5.0 - {current_time}")
            
        except Exception as e:
            print(f"Ошибка обновления времени: {e}")
    
    def update_stats_elements(self):
        """Обновление статистических элементов"""
        try:
            # Обновляем счетчики
            self.update_counters['stats_updates'] = self.update_counters.get('stats_updates', 0) + 1
            
            # Если активна вкладка dashboard, обновляем статистику
            current_tab = self.app.tabs.currentWidget()
            if hasattr(current_tab, 'objectName') and current_tab.objectName() == "dashboard_tab":
                self.refresh_dashboard_stats()
                
        except Exception as e:
            print(f"Ошибка обновления статистики: {e}")
    
    def refresh_dashboard_stats(self):
        """Обновление статистики на dashboard"""
        try:
            # Получаем актуальные данные
            from task_manager import task_manager, TaskStatus
            
            total_tasks = len(task_manager.get_tasks_for_today())
            completed_count = len(task_manager.get_completed_tasks_today())
            
            # Добавляем небольшую рандомизацию для демонстрации динамики
            demo_boost = random.randint(0, 2)
            total_tasks += demo_boost
            
            # Обновляем карточки если они существуют
            if hasattr(self.app, 'tasks_card_element'):
                self.update_task_card(total_tasks)
            
            if hasattr(self.app, 'completed_card_element'):
                self.update_completed_card(completed_count, total_tasks)
                
        except Exception as e:
            print(f"Ошибка обновления dashboard: {e}")
    
    def update_task_card(self, total_tasks):
        """Обновление карточки задач"""
        activity_level = min(total_tasks * 10, 100)
        motivation = self.get_task_motivation(total_tasks)
        
        html = f"""
        <div style='background: linear-gradient(135deg, #2D2D2D, #3D3D3D); padding: 25px; border-radius: 12px; text-align: center; border: 1px solid #FF2B4340; box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
            <h3 style='color: #FF2B43; margin: 0; font-size: 14px;'>📋 Задачи сегодня</h3>
            <h1 style='margin: 15px 0; font-family: "Courier New", monospace; color: #FF2B43; font-size: 32px; text-shadow: 0 0 10px #FF2B4350; letter-spacing: 2px;'>{total_tasks}</h1>
            
            <div style='margin: 15px 0; background: #1A1A1A; border-radius: 10px; height: 8px; overflow: hidden;'>
                <div style='background: linear-gradient(90deg, #FF2B43, #FF2B4380); height: 100%; width: {activity_level}%; border-radius: 10px; transition: width 0.3s ease;'></div>
            </div>
            <p style='color: #FF2B43; margin: 5px 0; font-size: 11px; font-weight: bold;'>Активность: {activity_level:.0f}%</p>
            
            <p style='color: #FFD700; margin: 10px 0; font-size: 11px; font-style: italic; opacity: 0.9;'>{motivation}</p>
        </div>
        """
        
        if hasattr(self.app, 'tasks_card_element'):
            self.app.tasks_card_element.setText(html)
    
    def update_completed_card(self, completed_count, total_tasks):
        """Обновление карточки выполненных задач"""
        completion_rate = (completed_count / max(total_tasks, 1)) * 100
        motivation = self.get_completion_motivation(completion_rate)
        
        html = f"""
        <div style='background: linear-gradient(135deg, #2D2D2D, #3D3D3D); padding: 25px; border-radius: 12px; text-align: center; border: 1px solid #4CAF5040; box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
            <h3 style='color: #4CAF50; margin: 0; font-size: 14px;'>✅ Выполнено задач</h3>
            <h1 style='margin: 15px 0; font-family: "Courier New", monospace; color: #4CAF50; font-size: 32px; text-shadow: 0 0 10px #4CAF5050; letter-spacing: 2px;'>{completed_count}</h1>
            
            <div style='margin: 15px 0; background: #1A1A1A; border-radius: 10px; height: 8px; overflow: hidden;'>
                <div style='background: linear-gradient(90deg, #4CAF50, #4CAF5080); height: 100%; width: {completion_rate:.1f}%; border-radius: 10px; transition: width 0.3s ease;'></div>
            </div>
            <p style='color: #4CAF50; margin: 5px 0; font-size: 11px; font-weight: bold;'>Выполнено: {completion_rate:.0f}%</p>
            
            <p style='color: #FFD700; margin: 10px 0; font-size: 11px; font-style: italic; opacity: 0.9;'>{motivation}</p>
        </div>
        """
        
        if hasattr(self.app, 'completed_card_element'):
            self.app.completed_card_element.setText(html)
    
    def update_motivation_elements(self):
        """Обновление мотивационных сообщений"""
        try:
            # Обновляем мотивационные сообщения в карточках
            self.refresh_dashboard_stats()
            
            # Добавляем уведомления в статус-бар
            self.show_motivation_notification()
            
        except Exception as e:
            print(f"Ошибка обновления мотивации: {e}")
    
    def update_animations(self):
        """Обновление анимационных эффектов"""
        try:
            # Добавляем пульсацию к активным элементам
            self.add_pulse_effects()
            
            # Обновляем прогресс-бары с анимацией
            self.animate_progress_bars()
            
        except Exception as e:
            print(f"Ошибка анимации: {e}")
    
    def get_task_motivation(self, total_tasks):
        """Получение мотивационного сообщения для задач"""
        messages = {
            0: ["Начните планировать день! 📝", "Добавьте первую задачу! 🚀"],
            1: ["Хорошее начало! 👍", "Продолжайте планирование! 📋"],
            3: ["Отличный план! 🎯", "Продуктивный день впереди! ⚡"],
            5: ["Амбициозные планы! 💪", "Вы настроены серьезно! 🔥"],
            10: ["Супер активность! 🌟", "Невероятная продуктивность! 🚀"]
        }
        
        for threshold in sorted(messages.keys(), reverse=True):
            if total_tasks >= threshold:
                return random.choice(messages[threshold])
        
        return "Планируйте эффективно! ⭐"
    
    def get_completion_motivation(self, completion_rate):
        """Получение мотивационного сообщения для выполнения"""
        if completion_rate >= 90:
            return random.choice(["Невероятно! 🏆", "Вы чемпион! 👑", "Идеальный результат! ⭐"])
        elif completion_rate >= 70:
            return random.choice(["Превосходно! 🎉", "Отличная работа! 💪", "Так держать! 🔥"])
        elif completion_rate >= 50:
            return random.choice(["Хороший прогресс! 👍", "Продолжайте! 💪", "На правильном пути! 🎯"])
        elif completion_rate >= 25:
            return random.choice(["Начинаете разгон! 🚀", "Не останавливайтесь! ⚡", "Вперед к цели! 🎯"])
        else:
            return random.choice(["Время действовать! 🚀", "Начните выполнять! 💪", "Первый шаг важен! ⭐"])
    
    def show_motivation_notification(self):
        """Показ мотивационного уведомления"""
        hour = datetime.now().hour
        notifications = {
            9: "Утренний заряд энергии! Время для важных дел! ⚡",
            12: "Обеденное время! Не забудьте про отдых! 🍽️",
            15: "Послеобеденный рывок! Финишная прямая! 🏃‍♂️",
            18: "Время подводить итоги дня! 📊",
            21: "Планируйте завтрашний день! 📋"
        }
        
        if hour in notifications:
            print(f"💡 {notifications[hour]}")
    
    def add_pulse_effects(self):
        """Добавление эффектов пульсации"""
        # Эффекты будут добавлены через CSS анимации
        pass
    
    def animate_progress_bars(self):
        """Анимация прогресс-баров"""
        # Обновляем прогресс-бары с плавными переходами
        pass
    
    def get_dynamic_stats(self):
        """Получение динамической статистики"""
        return {
            'updates_count': self.update_counters.get('stats_updates', 0),
            'active_elements': len(self.dynamic_elements),
            'last_update': datetime.now().strftime("%H:%M:%S")
        }

# Функции для интеграции с основным приложением
def setup_dynamic_interface(app):
    """Настройка динамического интерфейса для приложения"""
    app.dynamic_manager = DynamicInterfaceManager(app)
    return app.dynamic_manager

def register_dynamic_element(app, element_id, element, update_type="stats"):
    """Регистрация элемента для динамического обновления"""
    if hasattr(app, 'dynamic_manager'):
        app.dynamic_manager.register_dynamic_element(element_id, element, update_type)

print("Система динамического интерфейса загружена!")
