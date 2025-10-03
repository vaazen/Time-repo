# dynamic_elements.py - Дополнительные динамические элементы

import random
from datetime import datetime, timedelta

class DynamicTaskList:
    """Динамический список задач с живыми обновлениями"""
    
    def __init__(self):
        self.demo_tasks = [
            {"title": "Изучение Python", "time": "09:00", "status": "in_progress", "priority": "high"},
            {"title": "Встреча с командой", "time": "10:30", "status": "planned", "priority": "medium"},
            {"title": "Код-ревью", "time": "14:00", "status": "planned", "priority": "high"},
            {"title": "Документация API", "time": "15:30", "status": "planned", "priority": "low"},
            {"title": "Планирование спринта", "time": "17:00", "status": "planned", "priority": "medium"}
        ]
        self.last_update = datetime.now()
    
    def get_dynamic_task_text(self):
        """Генерирует динамический текст списка задач"""
        current_time = datetime.now()
        
        # Добавляем случайные изменения для демонстрации
        if random.random() < 0.3:  # 30% шанс изменения
            self.simulate_task_progress()
        
        task_text = "📋 Актуальные задачи:\n\n"
        
        for i, task in enumerate(self.demo_tasks[:5]):
            # Определяем иконку статуса
            status_icons = {
                "completed": "✅",
                "in_progress": "🔄", 
                "planned": "⏰",
                "overdue": "🚨"
            }
            
            # Определяем приоритет
            priority_colors = {
                "high": "🔴",
                "medium": "🟡", 
                "low": "🟢"
            }
            
            icon = status_icons.get(task["status"], "⏰")
            priority = priority_colors.get(task["priority"], "🟡")
            
            # Добавляем индикатор времени
            task_time = datetime.strptime(task["time"], "%H:%M").time()
            current_time_only = current_time.time()
            
            time_indicator = ""
            if task_time < current_time_only and task["status"] == "planned":
                time_indicator = " (просрочено)"
                icon = "🚨"
            elif task_time <= current_time_only and task["status"] == "in_progress":
                time_indicator = " (сейчас)"
            
            task_text += f"{icon} {priority} {task['title']} ({task['time']}){time_indicator}\n"
        
        # Добавляем статистику
        completed = len([t for t in self.demo_tasks if t["status"] == "completed"])
        total = len(self.demo_tasks)
        
        task_text += f"\n📊 Прогресс: {completed}/{total} задач выполнено"
        task_text += f"\n⏰ Обновлено: {current_time.strftime('%H:%M:%S')}"
        
        return task_text
    
    def simulate_task_progress(self):
        """Симулирует прогресс выполнения задач"""
        for task in self.demo_tasks:
            if task["status"] == "planned" and random.random() < 0.1:
                task["status"] = "in_progress"
            elif task["status"] == "in_progress" and random.random() < 0.2:
                task["status"] = "completed"

class DynamicChart:
    """Динамический график с анимированными данными"""
    
    def __init__(self):
        self.base_data = [3, 5, 4, 7, 6, 8, 5]  # Базовые данные по дням
        self.last_update = datetime.now()
    
    def get_dynamic_chart_text(self):
        """Генерирует динамический текст графика"""
        current_time = datetime.now()
        
        # Добавляем небольшие колебания к данным
        animated_data = []
        for base_value in self.base_data:
            variation = random.randint(-1, 2)
            new_value = max(0, min(10, base_value + variation))
            animated_data.append(new_value)
        
        chart_text = "📈 Динамическая продуктивность:\n\n"
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        
        max_value = max(animated_data) if animated_data else 10
        
        for i, (day, value) in enumerate(zip(days, animated_data)):
            # Создаем анимированную визуализацию
            bar_length = int((value / max_value) * 10)
            bar = "█" * bar_length + "░" * (10 - bar_length)
            
            # Добавляем цветовую индикацию
            if value >= 8:
                indicator = "🔥"  # Высокая продуктивность
            elif value >= 6:
                indicator = "⚡"  # Хорошая продуктивность
            elif value >= 4:
                indicator = "👍"  # Средняя продуктивность
            else:
                indicator = "📈"  # Низкая продуктивность
            
            # Выделяем текущий день
            if i == current_time.weekday():
                day_marker = f"[{day}]"  # Текущий день в скобках
            else:
                day_marker = f" {day} "
            
            chart_text += f"{day_marker}: {bar} {indicator} ({value}/10)\n"
        
        # Добавляем общую статистику
        avg_productivity = sum(animated_data) / len(animated_data)
        trend = "📈" if animated_data[-1] > animated_data[-2] else "📉"
        
        chart_text += f"\n📊 Средняя продуктивность: {avg_productivity:.1f}/10"
        chart_text += f"\n{trend} Тренд: {'Рост' if animated_data[-1] > animated_data[-2] else 'Снижение'}"
        chart_text += f"\n🕐 Обновлено: {current_time.strftime('%H:%M:%S')}"
        
        return chart_text

class DynamicStats:
    """Динамическая детальная статистика"""
    
    def __init__(self):
        self.session_start = datetime.now()
        self.update_count = 0
    
    def get_dynamic_stats_text(self):
        """Генерирует динамический текст статистики"""
        current_time = datetime.now()
        self.update_count += 1
        
        # Вычисляем время сессии
        session_duration = current_time - self.session_start
        session_minutes = int(session_duration.total_seconds() / 60)
        
        # Генерируем динамические метрики
        focus_time = random.randint(45, 95)
        interruptions = random.randint(0, 5)
        productivity_score = random.randint(75, 98)
        
        stats_text = f"""🔄 Живая статистика сессии:

⏱️ Время работы: {session_minutes} мин
🎯 Фокус: {focus_time}%
🚫 Прерывания: {interruptions}
📊 Продуктивность: {productivity_score}%

📈 Динамические метрики:
• Обновлений интерфейса: {self.update_count}
• Активное время: {session_minutes} мин
• Эффективность: {'Высокая' if productivity_score > 85 else 'Средняя'}
• Статус: {'В потоке' if focus_time > 80 else 'Концентрация'}

🎯 Рекомендации:
{self.get_dynamic_recommendations(focus_time, productivity_score)}

🕐 Последнее обновление: {current_time.strftime('%H:%M:%S')}"""
        
        return stats_text
    
    def get_dynamic_recommendations(self, focus_time, productivity_score):
        """Генерирует динамические рекомендации"""
        recommendations = []
        
        if focus_time < 60:
            recommendations.append("• Уберите отвлекающие факторы")
        if productivity_score < 80:
            recommendations.append("• Сделайте короткий перерыв")
        if self.update_count > 50:
            recommendations.append("• Отличная активность!")
        
        if not recommendations:
            recommendations.append("• Продолжайте в том же духе!")
        
        return "\n".join(recommendations)

# Глобальные экземпляры для использования
dynamic_task_list = DynamicTaskList()
dynamic_chart = DynamicChart()
dynamic_stats = DynamicStats()

print("Динамические элементы загружены!")
