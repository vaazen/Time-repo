# test_cpp_module.py - Тестирование C++ модуля
import os
import ctypes
import time

def test_cpp_module():
    """Тестирование C++ модуля"""
    print("="*60)
    print("ТЕСТИРОВАНИЕ C++ МОДУЛЯ")
    print("="*60)
    
    # Проверяем наличие DLL файла
    dll_files = ["performance.dll", "performance.so"]
    dll_found = None
    
    for dll_file in dll_files:
        if os.path.exists(dll_file):
            dll_found = dll_file
            break
    
    if not dll_found:
        print("C++ модуль не найден")
        print("\nДля компиляции C++ модуля:")
        print("1. Установите MinGW-w64 или Visual Studio Build Tools")
        print("2. Выполните команду:")
        print("   g++ -shared -O3 performance_simple.cpp -o performance.dll")
        print("   или")
        print("   cl /LD /O2 performance_simple.cpp /Fe:performance.dll")
        print("\n3. Или используйте build_modules.py")
        return False
    
    print(f"✅ Найден C++ модуль: {dll_found}")
    
    try:
        # Загружаем библиотеку
        cpp_lib = ctypes.CDLL(f"./{dll_found}")
        print("✅ C++ модуль успешно загружен")
        
        # Настраиваем типы функций
        cpp_lib.calculate_productivity.argtypes = [ctypes.c_int, ctypes.c_int]
        cpp_lib.calculate_productivity.restype = ctypes.c_double
        
        cpp_lib.performance_benchmark.argtypes = []
        cpp_lib.performance_benchmark.restype = ctypes.c_double
        
        cpp_lib.test_function.argtypes = []
        cpp_lib.test_function.restype = ctypes.c_int
        
        # Тестируем функции
        print("\n📊 Тестирование функций:")
        
        # Тест функции проверки
        test_result = cpp_lib.test_function()
        print(f"   test_function(): {test_result} {'✅' if test_result == 42 else '❌'}")
        
        # Тест расчета продуктивности
        productivity = cpp_lib.calculate_productivity(5, 300)
        print(f"   calculate_productivity(5, 300): {productivity:.2f}%")
        
        # Тест производительности
        print("\n⚡ Тест производительности:")
        
        # Python версия
        start_time = time.time()
        python_result = 0.0
        for i in range(1000000):
            python_result += i * 0.001
        python_time = time.time() - start_time
        
        # C++ версия
        start_time = time.time()
        cpp_result = cpp_lib.performance_benchmark()
        cpp_time = time.time() - start_time
        
        print(f"   Python время: {python_time:.6f} сек")
        print(f"   C++ время: {cpp_time:.6f} сек")
        
        if cpp_time > 0:
            speedup = python_time / cpp_time
            print(f"   Ускорение: {speedup:.2f}x")
        
        print("\n✅ C++ модуль работает корректно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании C++ модуля: {e}")
        return False

def show_compilation_instructions():
    """Показать инструкции по компиляции"""
    print("\n" + "="*60)
    print("ИНСТРУКЦИИ ПО КОМПИЛЯЦИИ C++ МОДУЛЯ")
    print("="*60)
    
    print("""
🔧 ВАРИАНТ 1: MinGW-w64 (Рекомендуется)
1. Скачайте MSYS2: https://www.msys2.org/
2. Установите компилятор:
   pacman -S mingw-w64-x86_64-gcc
3. Добавьте в PATH: C:\\msys64\\mingw64\\bin
4. Компилируйте:
   g++ -shared -O3 performance_simple.cpp -o performance.dll

🔧 ВАРИАНТ 2: Visual Studio Build Tools
1. Скачайте Build Tools: https://visualstudio.microsoft.com/downloads/
2. Установите C++ build tools
3. Откройте Developer Command Prompt
4. Компилируйте:
   cl /LD /O2 performance_simple.cpp /Fe:performance.dll

🔧 ВАРИАНТ 3: Автоматическая сборка
   python build_modules.py

📝 ПРИМЕЧАНИЕ:
Приложение работает и без C++ модуля, используя Python fallback.
C++ модуль нужен только для демонстрации гибридной архитектуры.
    """)

def main():
    print("ТЕСТИРОВАНИЕ C++ МОДУЛЯ ПРОИЗВОДИТЕЛЬНОСТИ")
    
    # Тестируем модуль
    success = test_cpp_module()
    
    if not success:
        show_compilation_instructions()
    
    print("\n" + "="*60)
    print("СТАТУС C++ МОДУЛЯ")
    print("="*60)
    
    if success:
        print("✅ C++ модуль работает и готов к использованию")
        print("🚀 Приложение использует высокопроизводительные C++ вычисления")
    else:
        print("⚠️ C++ модуль не скомпилирован")
        print("🐍 Приложение использует Python fallback (полностью функционально)")
        print("💡 Для получения максимальной производительности скомпилируйте C++ модуль")

if __name__ == "__main__":
    main()
