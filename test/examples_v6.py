"""
📚 Примеры использования новых возможностей Time Blocking v6.0
Демонстрирует практическое применение всех улучшений
"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Dict

# Импорты новых модулей
from config_manager import get_config, update_config
from cache_manager import cached, get_cache_manager
from async_notifications import (
    get_notification_manager, create_task_reminder, 
    create_break_suggestion, NotificationRule
)

class ProductivityAnalyzer:
    """Пример использования кэширования для анализа продуктивности"""
    
    def __init__(self):
        self.cache = get_cache_manager()
    
    @cached(ttl=300, use_file_cache=True)  # Кэшируем на 5 минут
    def analyze_daily_productivity(self, date: str) -> Dict:
        """Анализ продуктивности за день (тяжелая операция)"""
        print(f"Выполняем анализ продуктивности за {date}...")
        
        # Имитируем тяжелые вычисления
        import time
        time.sleep(2)
        
        # Возвращаем результат анализа
        return {
            "date": date,
            "total_tasks": 15,
            "completed_tasks": 12,
            "productivity_score": 80,
            "focus_time_minutes": 240,
            "break_time_minutes": 60,
            "efficiency_rating": "Высокая"
        }
    
    @cached(ttl=60)  # Кэшируем на 1 минуту
    def get_current_stats(self) -> Dict:
        """Получение текущей статистики"""
        return {
            "active_tasks": 3,
            "completed_today": 8,
            "time_spent": 180,  # минуты
            "current_focus_session": 45
        }

class SmartNotificationSystem:
    """Пример использования умной системы уведомлений"""
    
    def __init__(self):
        self.notification_manager = get_notification_manager()
        self.setup_rules()
    
    def setup_rules(self):
        """Настройка правил уведомлений"""
        
        # Правило для напоминания о перерывах
        break_rule = NotificationRule(
            name="break_reminder",
            condition=self.should_suggest_break,
            notification_factory=self.create_break_notification
        )
        
        # Правило для напоминания о дедлайнах
        deadline_rule = NotificationRule(
            name="deadline_warning",
            condition=self.has_approaching_deadlines,
            notification_factory=self.create_deadline_notification
        )
        
        self.notification_manager.add_rule(break_rule)
        self.notification_manager.add_rule(deadline_rule)
    
    def should_suggest_break(self) -> bool:
        """Проверка, нужен ли перерыв"""
        # Логика определения необходимости перерыва
        stats = ProductivityAnalyzer().get_current_stats()
        return stats["current_focus_session"] >= 90  # 90 минут непрерывной работы
    
    def has_approaching_deadlines(self) -> bool:
        """Проверка приближающихся дедлайнов"""
        # Логика проверки дедлайнов
        return datetime.now().hour in [9, 14, 18]  # Проверяем в определенное время
    
    def create_break_notification(self):
        """Создание уведомления о перерыве"""
        stats = ProductivityAnalyzer().get_current_stats()
        return create_break_suggestion(stats["current_focus_session"])
    
    def create_deadline_notification(self):
        """Создание уведомления о дедлайне"""
        from async_notifications import create_deadline_warning
        return create_deadline_warning("Важный проект", 4)  # 4 часа до дедлайна

class ConfigurableTaskManager:
    """Пример использования системы конфигурации"""
    
    def __init__(self):
        self.config = get_config()
        self.tasks = []
    
    def create_task(self, title: str, description: str = "") -> Dict:
        """Создание задачи с учетом конфигурации"""
        task = {
            "id": f"task_{len(self.tasks) + 1}",
            "title": title,
            "description": description,
            "created_at": datetime.now(),
            "priority": "medium",
            "estimated_duration": self.config.ui.auto_save_interval * 2  # Используем настройку
        }
        
        self.tasks.append(task)
        
        # Автосохранение, если включено
        if self.config.data.backup_enabled:
            self.save_tasks()
        
        return task
    
    def save_tasks(self):
        """Сохранение задач"""
        print(f"Сохраняем задачи (формат: {self.config.data.export_format})")
        # Логика сохранения
    
    def get_ui_settings(self) -> Dict:
        """Получение настроек UI"""
        return {
            "theme": self.config.ui.theme,
            "language": self.config.ui.language,
            "animations": self.config.ui.animations_enabled,
            "font_size": self.config.ui.font_size
        }

class PerformanceOptimizedApp:
    """Пример оптимизированного приложения"""
    
    def __init__(self):
        self.config = get_config()
        self.cache = get_cache_manager()
        self.analyzer = ProductivityAnalyzer()
        self.notifications = SmartNotificationSystem()
        self.task_manager = ConfigurableTaskManager()
    
    async def run_daily_analysis(self):
        """Запуск ежедневного анализа"""
        print("Запуск ежедневного анализа...")
        
        # Получаем данные за последние 7 дней
        tasks = []
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            
            # Благодаря кэшированию, повторные запросы будут мгновенными
            analysis = self.analyzer.analyze_daily_productivity(date)
            tasks.append(analysis)
        
        print(f"Анализ завершен для {len(tasks)} дней")
        return tasks
    
    def demonstrate_caching(self):
        """Демонстрация работы кэширования"""
        print("\nДемонстрация кэширования:")
        
        import time
        
        # Первый вызов - медленный (без кэша)
        start_time = time.time()
        result1 = self.analyzer.analyze_daily_productivity("2024-01-15")
        first_call_time = time.time() - start_time
        
        # Второй вызов - быстрый (из кэша)
        start_time = time.time()
        result2 = self.analyzer.analyze_daily_productivity("2024-01-15")
        second_call_time = time.time() - start_time
        
        print(f"Первый вызов: {first_call_time:.3f} сек")
        print(f"Второй вызов: {second_call_time:.3f} сек")
        
        # Избегаем деления на ноль
        if second_call_time > 0:
            speedup = first_call_time / second_call_time
            print(f"Ускорение: {speedup:.1f}x")
        else:
            print("Ускорение: >1000x (второй вызов мгновенный)")
        
        # Статистика кэша
        stats = self.cache.get_stats()
        print(f"Статистика кэша: {stats['memory_cache']['hit_rate']:.1f}% попаданий")
    
    def demonstrate_notifications(self):
        """Демонстрация системы уведомлений"""
        print("\nДемонстрация уведомлений:")
        
        # Отправляем различные типы уведомлений
        notifications = [
            create_task_reminder("task_1", "Завершить отчет", datetime.now()),
            create_break_suggestion(120),  # 2 часа работы
        ]
        
        for notification in notifications:
            self.notifications.notification_manager.send_notification_sync(notification)
            print(f"Отправлено: {notification.title}")
    
    def demonstrate_configuration(self):
        """Демонстрация системы конфигурации"""
        print("\nДемонстрация конфигурации:")
        
        # Показываем текущие настройки
        ui_settings = self.task_manager.get_ui_settings()
        print(f"Текущая тема: {ui_settings['theme']}")
        print(f"Язык: {ui_settings['language']}")
        print(f"Анимации: {ui_settings['animations']}")
        
        # Изменяем настройки
        print("Изменяем тему на светлую...")
        # Обновляем только отдельные поля, не весь объект
        self.config.ui.theme = 'light'
        
        # Создаем задачу с новыми настройками
        task = self.task_manager.create_task(
            "Тестовая задача",
            "Демонстрация работы с конфигурацией"
        )
        print(f"Создана задача: {task['title']}")

async def main():
    """Главная функция демонстрации"""
    print("Time Blocking v6.0 - Демонстрация улучшений")
    print("=" * 50)
    
    # Создаем приложение
    app = PerformanceOptimizedApp()
    
    # Демонстрируем возможности
    app.demonstrate_configuration()
    app.demonstrate_caching()
    app.demonstrate_notifications()
    
    # Запускаем асинхронный анализ
    await app.run_daily_analysis()
    
    print("\nДемонстрация завершена!")
    print("\nОсновные улучшения v6.0:")
    print("• Централизованная конфигурация")
    print("• Многоуровневое кэширование") 
    print("• Асинхронные уведомления")
    print("• Современный UI")
    print("• Улучшенная производительность")

if __name__ == "__main__":
    # Запускаем демонстрацию
    asyncio.run(main())
