"""
💾 Система кэширования для улучшения производительности
Обеспечивает быстрый доступ к часто используемым данным
"""

import json
import pickle
import hashlib
import time
from typing import Any, Optional, Dict, Callable, Union
from pathlib import Path
from datetime import datetime, timedelta
import threading
import logging
from functools import wraps
import weakref

class CacheEntry:
    """Запись в кэше"""
    
    def __init__(self, value: Any, ttl: Optional[float] = None):
        self.value = value
        self.created_at = time.time()
        self.ttl = ttl
        self.access_count = 0
        self.last_accessed = self.created_at
    
    def is_expired(self) -> bool:
        """Проверка истечения срока действия"""
        if self.ttl is None:
            return False
        return time.time() - self.created_at > self.ttl
    
    def access(self) -> Any:
        """Доступ к значению с обновлением статистики"""
        self.access_count += 1
        self.last_accessed = time.time()
        return self.value

class MemoryCache:
    """Кэш в памяти с поддержкой TTL и LRU"""
    
    def __init__(self, max_size: int = 1000, default_ttl: Optional[float] = None):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = threading.RLock()
        self.logger = logging.getLogger(__name__)
        
        # Статистика
        self.hits = 0
        self.misses = 0
        self.evictions = 0
    
    def get(self, key: str) -> Optional[Any]:
        """Получение значения из кэша"""
        with self._lock:
            if key not in self._cache:
                self.misses += 1
                return None
            
            entry = self._cache[key]
            
            if entry.is_expired():
                del self._cache[key]
                self.misses += 1
                return None
            
            self.hits += 1
            return entry.access()
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """Установка значения в кэш"""
        with self._lock:
            if ttl is None:
                ttl = self.default_ttl
            
            # Проверяем размер кэша
            if len(self._cache) >= self.max_size and key not in self._cache:
                self._evict_lru()
            
            self._cache[key] = CacheEntry(value, ttl)
    
    def delete(self, key: str) -> bool:
        """Удаление значения из кэша"""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def clear(self) -> None:
        """Очистка кэша"""
        with self._lock:
            self._cache.clear()
            self.hits = 0
            self.misses = 0
            self.evictions = 0
    
    def _evict_lru(self) -> None:
        """Удаление наименее используемого элемента"""
        if not self._cache:
            return
        
        # Находим элемент с наименьшим временем последнего доступа
        lru_key = min(self._cache.keys(), 
                     key=lambda k: self._cache[k].last_accessed)
        
        del self._cache[lru_key]
        self.evictions += 1
    
    def cleanup_expired(self) -> int:
        """Очистка истекших записей"""
        with self._lock:
            expired_keys = [key for key, entry in self._cache.items() 
                          if entry.is_expired()]
            
            for key in expired_keys:
                del self._cache[key]
            
            return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """Получение статистики кэша"""
        with self._lock:
            total_requests = self.hits + self.misses
            hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
            
            return {
                'size': len(self._cache),
                'max_size': self.max_size,
                'hits': self.hits,
                'misses': self.misses,
                'evictions': self.evictions,
                'hit_rate': hit_rate
            }

class FileCache:
    """Файловый кэш для долговременного хранения"""
    
    def __init__(self, cache_dir: str = "cache", max_size_mb: int = 100):
        self.cache_dir = Path(cache_dir) if isinstance(cache_dir, str) else cache_dir
        self.cache_dir.mkdir(exist_ok=True)
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.logger = logging.getLogger(__name__)
    
    def _get_file_path(self, key: str) -> Path:
        """Получение пути к файлу кэша"""
        # Создаем безопасное имя файла из ключа
        safe_key = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{safe_key}.cache"
    
    def get(self, key: str) -> Optional[Any]:
        """Получение значения из файлового кэша"""
        try:
            file_path = self._get_file_path(key)
            
            if not file_path.exists():
                return None
            
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
            
            # Проверяем TTL
            if 'ttl' in data and data['ttl'] is not None:
                if time.time() - data['created_at'] > data['ttl']:
                    file_path.unlink()  # Удаляем истекший файл
                    return None
            
            # Обновляем время доступа
            file_path.touch()
            
            return data['value']
            
        except Exception as e:
            self.logger.error(f"Ошибка чтения из файлового кэша: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> bool:
        """Установка значения в файловый кэш"""
        try:
            # Проверяем размер кэша
            self._cleanup_if_needed()
            
            file_path = self._get_file_path(key)
            
            data = {
                'value': value,
                'created_at': time.time(),
                'ttl': ttl
            }
            
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка записи в файловый кэш: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Удаление значения из файлового кэша"""
        try:
            file_path = self._get_file_path(key)
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            self.logger.error(f"Ошибка удаления из файлового кэша: {e}")
            return False
    
    def clear(self) -> None:
        """Очистка файлового кэша"""
        try:
            for file_path in self.cache_dir.glob("*.cache"):
                file_path.unlink()
        except Exception as e:
            self.logger.error(f"Ошибка очистки файлового кэша: {e}")
    
    def _cleanup_if_needed(self) -> None:
        """Очистка кэша при превышении размера"""
        try:
            total_size = sum(f.stat().st_size for f in self.cache_dir.glob("*.cache"))
            
            if total_size > self.max_size_bytes:
                # Удаляем самые старые файлы
                files = list(self.cache_dir.glob("*.cache"))
                files.sort(key=lambda f: f.stat().st_atime)
                
                while total_size > self.max_size_bytes * 0.8 and files:
                    file_to_remove = files.pop(0)
                    total_size -= file_to_remove.stat().st_size
                    file_to_remove.unlink()
                    
        except Exception as e:
            self.logger.error(f"Ошибка очистки файлового кэша: {e}")

class CacheManager:
    """Менеджер кэширования с поддержкой многоуровневого кэша"""
    
    def __init__(self, memory_cache_size: int = 1000, 
                 file_cache_size_mb: int = 100,
                 default_ttl: Optional[float] = None):
        
        self.memory_cache = MemoryCache(memory_cache_size, default_ttl)
        self.file_cache = FileCache(max_size_mb=file_cache_size_mb)
        self.logger = logging.getLogger(__name__)
        
        # Запускаем фоновую очистку
        self._start_cleanup_thread()
    
    def get(self, key: str, use_file_cache: bool = True) -> Optional[Any]:
        """Получение значения из кэша (сначала память, потом файл)"""
        # Сначала проверяем память
        value = self.memory_cache.get(key)
        if value is not None:
            return value
        
        # Затем проверяем файловый кэш
        if use_file_cache:
            value = self.file_cache.get(key)
            if value is not None:
                # Загружаем в память для быстрого доступа
                self.memory_cache.set(key, value)
                return value
        
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None,
            use_file_cache: bool = True) -> None:
        """Установка значения в кэш"""
        # Всегда сохраняем в память
        self.memory_cache.set(key, value, ttl)
        
        # Опционально сохраняем в файл
        if use_file_cache:
            self.file_cache.set(key, value, ttl)
    
    def delete(self, key: str) -> bool:
        """Удаление значения из всех уровней кэша"""
        memory_deleted = self.memory_cache.delete(key)
        file_deleted = self.file_cache.delete(key)
        return memory_deleted or file_deleted
    
    def clear(self) -> None:
        """Очистка всех уровней кэша"""
        self.memory_cache.clear()
        self.file_cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Получение статистики кэширования"""
        return {
            'memory_cache': self.memory_cache.get_stats(),
            'file_cache_dir': str(self.file_cache.cache_dir),
            'file_cache_size_mb': self.file_cache.max_size_bytes / (1024 * 1024)
        }
    
    def _start_cleanup_thread(self) -> None:
        """Запуск фонового потока очистки"""
        def cleanup_worker():
            while True:
                try:
                    time.sleep(300)  # Каждые 5 минут
                    expired_count = self.memory_cache.cleanup_expired()
                    if expired_count > 0:
                        self.logger.debug(f"Очищено {expired_count} истекших записей из кэша")
                except Exception as e:
                    self.logger.error(f"Ошибка в фоновой очистке кэша: {e}")
        
        cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
        cleanup_thread.start()

# Декоратор для кэширования результатов функций
def cached(ttl: Optional[float] = None, use_file_cache: bool = False, 
          key_func: Optional[Callable] = None):
    """
    Декоратор для кэширования результатов функций
    
    Args:
        ttl: Время жизни кэша в секундах
        use_file_cache: Использовать файловый кэш
        key_func: Функция для генерации ключа кэша
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Генерируем ключ кэша
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Используем имя функции и хэш аргументов
                args_str = str(args) + str(sorted(kwargs.items()))
                cache_key = f"{func.__name__}:{hashlib.md5(args_str.encode()).hexdigest()}"
            
            # Проверяем кэш
            cached_result = cache_manager.get(cache_key, use_file_cache)
            if cached_result is not None:
                return cached_result
            
            # Выполняем функцию и кэшируем результат
            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result, ttl, use_file_cache)
            
            return result
        
        # Добавляем методы для управления кэшем
        wrapper.clear_cache = lambda: cache_manager.clear()
        wrapper.cache_stats = lambda: cache_manager.get_stats()
        
        return wrapper
    return decorator

# Глобальный экземпляр менеджера кэша
cache_manager = CacheManager()

def get_cache_manager() -> CacheManager:
    """Получение глобального менеджера кэша"""
    return cache_manager
