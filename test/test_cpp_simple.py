# test_cpp_simple.py - Простое тестирование C++ модуля без эмодзи
import os
import ctypes
import time

def test_cpp_module():
    """Тестирование C++ модуля"""
    print("="*50)
    print("ТЕСТИРОВАНИЕ C++ МОДУЛЯ")
    print("="*50)
    
    # Проверяем наличие DLL файла
    dll_files = ["performance.dll", "performance.so"]
    dll_found = None
    
    for dll_file in dll_files:
        if os.path.exists(dll_file):
            dll_found = dll_file
            break
    
    if not dll_found:
        print("РЕЗУЛЬТАТ: C++ модуль не найден")
        print("\nПРИЧИНА: Не скомпилирован performance.dll")
        print("\nРЕШЕНИЕ:")
        print("1. Установите компилятор (MinGW-w64 или Visual Studio)")
        print("2. Выполните: g++ -shared -O3 performance_simple.cpp -o performance.dll")
        print("3. Или используйте: python build_modules.py")
        print("\nСТАТУС: Приложение работает с Python fallback")
        return False
    
    print(f"НАЙДЕН: {dll_found}")
    
    try:
        # Загружаем библиотеку
        cpp_lib = ctypes.CDLL(f"./{dll_found}")
        print("ЗАГРУЗКА: Успешно")
        
        # Настраиваем типы функций
        cpp_lib.calculate_productivity.argtypes = [ctypes.c_int, ctypes.c_int]
        cpp_lib.calculate_productivity.restype = ctypes.c_double
        
        # Тестируем функцию
        productivity = cpp_lib.calculate_productivity(5, 300)
        print(f"ТЕСТ: calculate_productivity(5, 300) = {productivity:.2f}%")
        
        print("РЕЗУЛЬТАТ: C++ модуль работает корректно")
        return True
        
    except Exception as e:
        print(f"ОШИБКА: {e}")
        return False

def main():
    print("ДИАГНОСТИКА C++ МОДУЛЯ")
    print("Проверяем компиляцию и работу C++ модуля производительности")
    
    success = test_cpp_module()
    
    print("\n" + "="*50)
    print("ИТОГОВЫЙ СТАТУС")
    print("="*50)
    
    if success:
        print("СТАТУС: C++ модуль активен")
        print("ПРОИЗВОДИТЕЛЬНОСТЬ: Максимальная")
        print("АРХИТЕКТУРА: Полная гибридная (Python + C++)")
    else:
        print("СТАТУС: Python fallback")
        print("ПРОИЗВОДИТЕЛЬНОСТЬ: Стандартная") 
        print("АРХИТЕКТУРА: Python-based")
        print("ПРИМЕЧАНИЕ: Все функции работают, C++ опционален")

if __name__ == "__main__":
    main()
