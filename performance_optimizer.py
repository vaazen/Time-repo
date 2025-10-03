# performance_optimizer.py - Оптимизация производительности
import json
import os
import pickle
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from functools import lru_cache
import threading
import queue
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer

class DataCache:
    """Система кэширования данных"""
    
    def __init__(self, max_size=1000, ttl_seconds=3600):
        self.cache = {}
        self.access_times = {}
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        
    def get(self, key: str) -> Optional[Any]:
        """Получение данных из кэша"""
        if key not in self.cache:
            return None
            
        # Проверяем TTL
        if self._is_expired(key):
            self.remove(key)
            return None
            
        self.access_times[key] = datetime.now()
        return self.cache[key]
    
    def set(self, key: str, value: Any):
        """Сохранение данных в кэш"""
        # Очищаем кэш если он переполнен
        if len(self.cache) >= self.max_size:
            self._cleanup()
            
        self.cache[key] = value
        self.access_times[key] = datetime.now()
    
    def remove(self, key: str):
        """Удаление из кэша"""
        self.cache.pop(key, None)
        self.access_times.pop(key, None)
    
    def _is_expired(self, key: str) -> bool:
        """Проверка истечения TTL"""
        if key not in self.access_times:
            return True
            
        age = datetime.now() - self.access_times[key]
        return age.total_seconds() > self.ttl_seconds
    
    def _cleanup(self):
        """Очистка устаревших записей"""
        expired_keys = [k for k in self.cache.keys() if self._is_expired(k)]
        for key in expired_keys:
            self.remove(key)
            
        # Если все еще переполнен, удаляем самые старые
        if len(self.cache) >= self.max_size:
            sorted_keys = sorted(self.access_times.items(), key=lambda x: x[1])
            for key, _ in sorted_keys[:len(self.cache) // 4]:  # Удаляем 25%
                self.remove(key)

class BackgroundProcessor(QThread):
    """Фоновый обработчик задач"""
    
    task_completed = pyqtSignal(str, object)  # task_id, result
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.task_queue = queue.Queue()
        self.running = True
        
    def add_task(self, task_id: str, func, *args, **kwargs):
        """Добавление задачи в очередь"""
        self.task_queue.put((task_id, func, args, kwargs))
    
    def run(self):
        """Основной цикл обработки"""
        while self.running:
            try:
                task_id, func, args, kwargs = self.task_queue.get(timeout=1)
                result = func(*args, **kwargs)
                self.task_completed.emit(task_id, result)
                self.task_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Ошибка выполнения фоновой задачи: {e}")
    
    def stop(self):
        """Остановка процессора"""
        self.running = False

class PerformanceOptimizer(QObject):
    """Главный класс оптимизации производительности"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cache = DataCache()
        self.background_processor = BackgroundProcessor()
        self.background_processor.start()
        self.cleanup_timer = None
        
        # Отложенная инициализация таймера
        self.init_cleanup_timer()
    
    def init_cleanup_timer(self):
        """Инициализация таймера очистки в правильном потоке"""
        from PyQt5.QtCore import QTimer
        if self.cleanup_timer is None:
            self.cleanup_timer = QTimer(self)
            self.cleanup_timer.timeout.connect(self._periodic_cleanup)
            self.cleanup_timer.start(300000)  # 5 минут
    
    @lru_cache(maxsize=128)
    def get_productivity_stats(self, date_str: str) -> Dict:
        """Кэшированное получение статистики продуктивности"""
        # Здесь будет реальная логика расчета статистики
        return {
            'productivity_score': 0.75,
            'completed_tasks': 8,
            'focus_time': 360,  # минуты
            'efficiency': 0.82
        }
    
    def preload_data(self, date_range: List[str]):
        """Предзагрузка данных в фоновом режиме"""
        for date_str in date_range:
            self.background_processor.add_task(
                f"preload_{date_str}",
                self._load_day_data,
                date_str
            )
    
    def _load_day_data(self, date_str: str) -> Dict:
        """Загрузка данных за день"""
        # Имитация загрузки данных
        return {
            'date': date_str,
            'tasks': [],
            'statistics': self.get_productivity_stats(date_str)
        }
    
    def _periodic_cleanup(self):
        """Периодическая очистка кэша и оптимизация"""
        # Очистка кэша
        self.cache._cleanup()
        
        # Очистка LRU кэша
        self.get_productivity_stats.cache_clear()
        
        print("Выполнена периодическая очистка кэша")

# Глобальный экземпляр оптимизатора (ленивая инициализация)
_performance_optimizer = None

def get_performance_optimizer():
    """Получение глобального экземпляра оптимизатора с ленивой инициализацией"""
    global _performance_optimizer
    if _performance_optimizer is None:
        _performance_optimizer = PerformanceOptimizer()
    return _performance_optimizer

# Для обратной совместимости
performance_optimizer = None
