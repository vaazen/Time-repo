# csharp_performance.py - Интерфейс для C# модуля производительности
import ctypes
import os
from typing import Optional

class CSharpPerformanceModule:
    """Интерфейс для C# модуля производительности"""
    
    def __init__(self):
        self.dll = None
        self.available = False
        self.load_module()
    
    def load_module(self):
        """Загрузка C# DLL модуля"""
        try:
            dll_path = "PerformanceModule.dll"
            if os.path.exists(dll_path):
                self.dll = ctypes.CDLL(dll_path)
                self.setup_function_signatures()
                self.available = True
                print("C# модуль производительности загружен успешно")
            else:
                print("C# модуль не найден, используется Python fallback")
        except Exception as e:
            print(f"Ошибка загрузки C# модуля: {e}")
            self.available = False
    
    def setup_function_signatures(self):
        """Настройка сигнатур функций C#"""
        if not self.dll:
            return
        
        # calculate_productivity
        self.dll.calculate_productivity.argtypes = [ctypes.c_int, ctypes.c_int]
        self.dll.calculate_productivity.restype = ctypes.c_double
        
        # calculate_efficiency
        self.dll.calculate_efficiency.argtypes = [ctypes.c_int, ctypes.c_int]
        self.dll.calculate_efficiency.restype = ctypes.c_double
        
        # performance_benchmark
        self.dll.performance_benchmark.argtypes = []
        self.dll.performance_benchmark.restype = ctypes.c_double
        
        # get_system_info
        self.dll.get_system_info.argtypes = []
        self.dll.get_system_info.restype = ctypes.c_char_p
        
        # free_string
        self.dll.free_string.argtypes = [ctypes.c_void_p]
        self.dll.free_string.restype = None
    
    def calculate_productivity(self, total_blocks: int, total_minutes: int) -> float:
        """Расчет продуктивности"""
        if self.available and self.dll:
            try:
                result = self.dll.calculate_productivity(total_blocks, total_minutes)
                return float(result)
            except Exception as e:
                print(f"Ошибка C# расчета: {e}")
        
        # Python fallback
        return self._python_calculate_productivity(total_blocks, total_minutes)
    
    def calculate_efficiency(self, total_blocks: int, total_minutes: int) -> float:
        """Расчет эффективности"""
        if self.available and self.dll:
            try:
                result = self.dll.calculate_efficiency(total_blocks, total_minutes)
                return float(result)
            except Exception as e:
                print(f"Ошибка C# расчета эффективности: {e}")
        
        # Python fallback
        return self._python_calculate_efficiency(total_blocks, total_minutes)
    
    def performance_benchmark(self) -> float:
        """Бенчмарк производительности"""
        if self.available and self.dll:
            try:
                result = self.dll.performance_benchmark()
                return float(result)
            except Exception as e:
                print(f"Ошибка C# бенчмарка: {e}")
        
        # Python fallback
        import time
        start_time = time.time()
        result = 0.0
        for i in range(100000):
            result += (i ** 0.5) * (i * 0.001)
        return (time.time() - start_time) * 1000  # в миллисекундах
    
    def get_system_info(self) -> str:
        """Получение информации о системе"""
        if self.available and self.dll:
            try:
                ptr = self.dll.get_system_info()
                if ptr:
                    info = ctypes.string_at(ptr).decode('ascii')
                    self.dll.free_string(ptr)
                    return info
            except Exception as e:
                print(f"Ошибка получения системной информации: {e}")
        
        # Python fallback
        import platform
        return f"Python Module Active|OS: {platform.system()} {platform.release()}|Python: {platform.python_version()}|Processors: {os.cpu_count()}"
    
    def _python_calculate_productivity(self, total_blocks: int, total_minutes: int) -> float:
        """Python fallback для расчета продуктивности"""
        if total_blocks == 0:
            return 0.0
        
        # Базовый расчет: 8 часов = 100% продуктивности
        base_productivity = (total_minutes / 480.0) * 100.0
        
        # Бонус за количество блоков
        block_bonus = min(20.0, total_blocks * 2.0)
        
        return min(100.0, base_productivity + block_bonus)
    
    def _python_calculate_efficiency(self, total_blocks: int, total_minutes: int) -> float:
        """Python fallback для расчета эффективности"""
        if total_blocks == 0:
            return 0.0
        
        avg_block_duration = total_minutes / total_blocks
        
        # Оптимальная длительность: 45-90 минут
        if 45 <= avg_block_duration <= 90:
            return 1.0
        elif avg_block_duration < 45:
            return avg_block_duration / 45.0
        else:
            return max(0.5, 90.0 / avg_block_duration)

# Глобальный экземпляр
csharp_performance = CSharpPerformanceModule()
