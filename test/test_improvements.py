"""
🧪 Тесты для проверки улучшений Time Blocking v6.0
Автоматическая проверка всех новых возможностей
"""

import unittest
import asyncio
import tempfile
import os
import json
import time
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Импорты тестируемых модулей
from config_manager import ConfigManager, AppConfig, UIConfig
from cache_manager import CacheManager, cached
from async_notifications import (
    AsyncNotificationManager, Notification, NotificationType, 
    NotificationPriority, NotificationChannel, create_task_reminder
)

class TestConfigManager(unittest.TestCase):
    """Тесты системы конфигурации"""
    
    def setUp(self):
        """Настройка тестов"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "test_config.json")
        self.config_manager = ConfigManager(self.config_path)
    
    def tearDown(self):
        """Очистка после тестов"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_default_config_creation(self):
        """Тест создания конфигурации по умолчанию"""
        config = self.config_manager.load_config()
        
        self.assertIsInstance(config, AppConfig)
        self.assertEqual(config.ui.language, "ru")
        self.assertEqual(config.ui.theme, "dark")
        self.assertTrue(config.ui.animations_enabled)
    
    def test_config_save_and_load(self):
        """Тест сохранения и загрузки конфигурации"""
        # Загружаем конфигурацию
        config = self.config_manager.load_config()
        
        # Изменяем настройки
        config.ui.language = "en"
        config.ui.theme = "light"
        config.ai.model = "gpt-4"
        
        # Сохраняем
        self.assertTrue(self.config_manager.save_config())
        
        # Создаем новый менеджер и загружаем
        new_manager = ConfigManager(self.config_path)
        loaded_config = new_manager.load_config()
        
        # Проверяем, что настройки сохранились
        self.assertEqual(loaded_config.ui.language, "en")
        self.assertEqual(loaded_config.ui.theme, "light")
        self.assertEqual(loaded_config.ai.model, "gpt-4")
    
    def test_env_variables_override(self):
        """Тест переопределения переменными окружения"""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_key_123',
            'DEBUG': 'true',
            'LOG_LEVEL': 'DEBUG'
        }):
            config = self.config_manager.load_config()
            
            self.assertEqual(config.ai.api_key, 'test_key_123')
            self.assertTrue(config.debug_mode)
            self.assertEqual(config.log_level, 'DEBUG')
    
    def test_config_update(self):
        """Тест обновления конфигурации"""
        # Обновляем настройки
        success = self.config_manager.update_config(
            debug_mode=True,
            log_level='INFO'
        )
        
        self.assertTrue(success)
        
        # Проверяем, что изменения применились
        config = self.config_manager.get_config()
        self.assertTrue(config.debug_mode)
        self.assertEqual(config.log_level, 'INFO')

class TestCacheManager(unittest.TestCase):
    """Тесты системы кэширования"""
    
    def setUp(self):
        """Настройка тестов"""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_manager = CacheManager(
            memory_cache_size=100,
            file_cache_size_mb=1
        )
        # Переопределяем директорию файлового кэша
        from pathlib import Path
        self.cache_manager.file_cache.cache_dir = Path(self.temp_dir)
    
    def tearDown(self):
        """Очистка после тестов"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_memory_cache_basic_operations(self):
        """Тест базовых операций кэша в памяти"""
        # Тестируем установку и получение
        self.cache_manager.set("test_key", "test_value")
        value = self.cache_manager.get("test_key")
        self.assertEqual(value, "test_value")
        
        # Тестируем несуществующий ключ
        value = self.cache_manager.get("nonexistent_key")
        self.assertIsNone(value)
        
        # Тестируем удаление
        self.assertTrue(self.cache_manager.delete("test_key"))
        value = self.cache_manager.get("test_key")
        self.assertIsNone(value)
    
    def test_cache_ttl(self):
        """Тест времени жизни кэша"""
        # Устанавливаем значение с коротким TTL
        self.cache_manager.set("ttl_key", "ttl_value", ttl=0.1)  # 0.1 секунды
        
        # Сразу должно быть доступно
        value = self.cache_manager.get("ttl_key")
        self.assertEqual(value, "ttl_value")
        
        # Ждем истечения TTL
        time.sleep(0.2)
        
        # Теперь должно быть None
        value = self.cache_manager.get("ttl_key")
        self.assertIsNone(value)
    
    def test_file_cache_operations(self):
        """Тест операций файлового кэша"""
        test_data = {"complex": "data", "numbers": [1, 2, 3]}
        
        # Сохраняем в файловый кэш
        self.cache_manager.set("file_key", test_data, use_file_cache=True)
        
        # Очищаем кэш в памяти
        self.cache_manager.memory_cache.clear()
        
        # Должны получить данные из файлового кэша
        value = self.cache_manager.get("file_key", use_file_cache=True)
        self.assertEqual(value, test_data)
    
    def test_cached_decorator(self):
        """Тест декоратора кэширования"""
        call_count = 0
        
        @cached(ttl=1.0)
        def expensive_function(x, y):
            nonlocal call_count
            call_count += 1
            return x + y
        
        # Первый вызов
        result1 = expensive_function(1, 2)
        self.assertEqual(result1, 3)
        self.assertEqual(call_count, 1)
        
        # Второй вызов с теми же аргументами (должен использовать кэш)
        result2 = expensive_function(1, 2)
        self.assertEqual(result2, 3)
        self.assertEqual(call_count, 1)  # Функция не должна вызываться повторно
        
        # Вызов с другими аргументами
        result3 = expensive_function(2, 3)
        self.assertEqual(result3, 5)
        self.assertEqual(call_count, 2)  # Функция должна вызваться
    
    def test_cache_statistics(self):
        """Тест статистики кэша"""
        # Добавляем данные
        self.cache_manager.set("key1", "value1")
        self.cache_manager.set("key2", "value2")
        
        # Делаем запросы
        self.cache_manager.get("key1")  # hit
        self.cache_manager.get("key1")  # hit
        self.cache_manager.get("key3")  # miss
        
        stats = self.cache_manager.get_stats()
        
        self.assertEqual(stats['memory_cache']['size'], 2)
        self.assertEqual(stats['memory_cache']['hits'], 2)
        self.assertEqual(stats['memory_cache']['misses'], 1)
        self.assertAlmostEqual(stats['memory_cache']['hit_rate'], 66.7, places=1)

class TestAsyncNotifications(unittest.TestCase):
    """Тесты асинхронной системы уведомлений"""
    
    def setUp(self):
        """Настройка тестов"""
        self.notification_manager = AsyncNotificationManager()
        # Останавливаем фоновый процессор для тестов
        self.notification_manager.running = False
    
    def test_notification_creation(self):
        """Тест создания уведомлений"""
        notification = create_task_reminder(
            "test_task",
            "Test Task Title",
            datetime.now()
        )
        
        self.assertEqual(notification.type, NotificationType.TASK_REMINDER)
        self.assertEqual(notification.priority, NotificationPriority.MEDIUM)
        self.assertEqual(notification.task_id, "test_task")
        self.assertIn("Test Task Title", notification.message)
    
    def test_notification_scheduling(self):
        """Тест планирования уведомлений"""
        future_time = datetime.now() + timedelta(minutes=5)
        notification = create_task_reminder(
            "scheduled_task",
            "Scheduled Task",
            future_time
        )
        
        # Планируем уведомление
        self.notification_manager.schedule_notification(notification)
        
        # Проверяем, что уведомление добавлено в список запланированных
        self.assertEqual(len(self.notification_manager.scheduled_notifications), 1)
        self.assertEqual(
            self.notification_manager.scheduled_notifications[0].id,
            notification.id
        )
    
    def test_notification_delivery_conditions(self):
        """Тест условий доставки уведомлений"""
        # Создаем уведомление с низким приоритетом
        low_priority_notification = Notification(
            id="test_low",
            type=NotificationType.BREAK_SUGGESTION,
            priority=NotificationPriority.LOW,
            title="Break Suggestion",
            message="Time for a break",
            channels=[NotificationChannel.SYSTEM_TRAY],
            scheduled_time=datetime.now(),
            created_at=datetime.now()
        )
        
        # Тестируем условия доставки
        should_deliver = self.notification_manager._should_deliver(low_priority_notification)
        self.assertIsInstance(should_deliver, bool)
    
    def test_notification_statistics(self):
        """Тест статистики уведомлений"""
        # Добавляем несколько уведомлений в историю
        for i in range(5):
            notification = create_task_reminder(
                f"task_{i}",
                f"Task {i}",
                datetime.now()
            )
            notification.delivered = True
            self.notification_manager.notification_history.append(notification)
        
        stats = self.notification_manager.get_statistics()
        
        self.assertEqual(stats['total'], 5)
        self.assertEqual(stats['delivered'], 5)
        self.assertEqual(stats['delivery_rate'], 100.0)
        self.assertIn('by_type', stats)
        self.assertIn('by_priority', stats)

class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""
    
    def setUp(self):
        """Настройка интеграционных тестов"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Создаем компоненты с временными файлами
        config_path = os.path.join(self.temp_dir, "integration_config.json")
        self.config_manager = ConfigManager(config_path)
        
        self.cache_manager = CacheManager(memory_cache_size=50, file_cache_size_mb=1)
        from pathlib import Path
        self.cache_manager.file_cache.cache_dir = Path(self.temp_dir)
        
        self.notification_manager = AsyncNotificationManager()
        self.notification_manager.running = False
    
    def tearDown(self):
        """Очистка после интеграционных тестов"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_config_cache_integration(self):
        """Тест интеграции конфигурации и кэширования"""
        # Загружаем конфигурацию
        config = self.config_manager.load_config()
        
        # Используем настройки кэша из конфигурации
        cache_enabled = config.data.cache_enabled
        cache_size = config.data.cache_size_mb
        
        self.assertTrue(cache_enabled)
        self.assertGreater(cache_size, 0)
        
        # Тестируем кэширование с учетом конфигурации
        if cache_enabled:
            self.cache_manager.set("config_test", "test_value")
            value = self.cache_manager.get("config_test")
            self.assertEqual(value, "test_value")
    
    def test_notifications_config_integration(self):
        """Тест интеграции уведомлений и конфигурации"""
        # Загружаем конфигурацию
        config = self.config_manager.load_config()
        
        # Проверяем настройки уведомлений
        notifications_enabled = config.ui.show_notifications
        
        # Создаем уведомление
        notification = create_task_reminder(
            "integration_task",
            "Integration Test Task",
            datetime.now()
        )
        
        # Проверяем, что настройки учитываются
        should_deliver = self.notification_manager._should_deliver(notification)
        
        if notifications_enabled:
            # Если уведомления включены, должно доставляться
            self.assertTrue(should_deliver or notification.priority == NotificationPriority.URGENT)
    
    def test_performance_with_all_components(self):
        """Тест производительности с всеми компонентами"""
        start_time = time.time()
        
        # Выполняем операции с конфигурацией
        config = self.config_manager.load_config()
        self.config_manager.save_config()
        
        # Выполняем операции с кэшем
        for i in range(10):
            self.cache_manager.set(f"perf_key_{i}", f"perf_value_{i}")
            self.cache_manager.get(f"perf_key_{i}")
        
        # Создаем уведомления
        for i in range(5):
            notification = create_task_reminder(
                f"perf_task_{i}",
                f"Performance Task {i}",
                datetime.now()
            )
            self.notification_manager.schedule_notification(notification)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Проверяем, что все операции выполняются быстро
        self.assertLess(execution_time, 1.0)  # Менее 1 секунды

class TestPerformanceImprovements(unittest.TestCase):
    """Тесты улучшений производительности"""
    
    def test_caching_performance_improvement(self):
        """Тест улучшения производительности благодаря кэшированию"""
        cache_manager = CacheManager()
        
        # Функция с искусственной задержкой
        @cached(ttl=60)
        def slow_function(x):
            time.sleep(0.1)  # Имитируем медленную операцию
            return x * 2
        
        # Первый вызов (медленный)
        start_time = time.time()
        result1 = slow_function(5)
        first_call_time = time.time() - start_time
        
        # Второй вызов (быстрый, из кэша)
        start_time = time.time()
        result2 = slow_function(5)
        second_call_time = time.time() - start_time
        
        # Проверяем результаты
        self.assertEqual(result1, result2)
        self.assertEqual(result1, 10)
        
        # Проверяем улучшение производительности
        self.assertGreater(first_call_time, 0.05)  # Первый вызов должен быть медленным
        self.assertLess(second_call_time, 0.01)    # Второй вызов должен быть быстрым
        
        # Ускорение должно быть значительным
        speedup = first_call_time / second_call_time
        self.assertGreater(speedup, 5)  # Минимум 5x ускорение

def run_all_tests():
    """Запуск всех тестов"""
    print("Запуск тестов Time Blocking v6.0")
    print("=" * 50)
    
    # Создаем test suite
    test_suite = unittest.TestSuite()
    
    # Добавляем тесты
    test_classes = [
        TestConfigManager,
        TestCacheManager,
        TestAsyncNotifications,
        TestIntegration,
        TestPerformanceImprovements
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Выводим результаты
    print("\n" + "=" * 50)
    print(f"Тестов запущено: {result.testsRun}")
    print(f"Ошибок: {len(result.errors)}")
    print(f"Неудач: {len(result.failures)}")
    
    if result.wasSuccessful():
        print("Все тесты прошли успешно!")
    else:
        print("Некоторые тесты не прошли")
        
        if result.errors:
            print("\nОшибки:")
            for test, error in result.errors:
                print(f"- {test}: {error}")
        
        if result.failures:
            print("\nНеудачи:")
            for test, failure in result.failures:
                print(f"- {test}: {failure}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
