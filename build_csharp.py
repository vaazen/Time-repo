# build_csharp.py - Сборка C# модуля производительности
import subprocess
import os
import sys

def check_dotnet():
    """Проверка наличия .NET SDK"""
    try:
        result = subprocess.run(['dotnet', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ .NET SDK найден: версия {version}")
            return True
        else:
            print("❌ .NET SDK не найден")
            return False
    except Exception as e:
        print(f"❌ Ошибка проверки .NET SDK: {e}")
        return False

def build_csharp_module():
    """Сборка C# модуля"""
    print("🔨 Начинаем сборку C# модуля...")
    
    try:
        # Сборка проекта
        result = subprocess.run(['dotnet', 'build', 'PerformanceModule.csproj', 
                               '--configuration', 'Release'],
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ C# модуль собран успешно")
            
            # Проверяем наличие DLL
            dll_paths = [
                "bin/Release/net6.0/PerformanceModule.dll",
                "PerformanceModule.dll"
            ]
            
            for dll_path in dll_paths:
                if os.path.exists(dll_path):
                    print(f"✅ Найден файл: {dll_path}")
                    
                    # Копируем в корень проекта если нужно
                    if dll_path != "PerformanceModule.dll":
                        import shutil
                        shutil.copy2(dll_path, "PerformanceModule.dll")
                        print("✅ DLL скопирован в корень проекта")
                    
                    return True
            
            print("⚠️ DLL файл не найден после сборки")
            return False
            
        else:
            print("❌ Ошибка сборки C# модуля:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Исключение при сборке: {e}")
        return False

def test_csharp_module():
    """Тестирование C# модуля"""
    print("🧪 Тестирование C# модуля...")
    
    try:
        from csharp_performance import csharp_performance
        
        if csharp_performance.available:
            print("✅ C# модуль загружен успешно")
            
            # Тест расчета продуктивности
            productivity = csharp_performance.calculate_productivity(5, 300)
            print(f"✅ Тест продуктивности: {productivity:.2f}%")
            
            # Тест эффективности
            efficiency = csharp_performance.calculate_efficiency(5, 300)
            print(f"✅ Тест эффективности: {efficiency:.2f}")
            
            # Тест бенчмарка
            benchmark = csharp_performance.performance_benchmark()
            print(f"✅ Бенчмарк: {benchmark:.2f} мс")
            
            # Системная информация
            sys_info = csharp_performance.get_system_info()
            print(f"✅ Системная информация: {sys_info}")
            
            return True
        else:
            print("❌ C# модуль не загружен, используется Python fallback")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

def show_instructions():
    """Показать инструкции по установке .NET"""
    print("\n" + "="*60)
    print("ИНСТРУКЦИИ ПО УСТАНОВКЕ .NET SDK")
    print("="*60)
    print("""
🔧 Для сборки C# модуля нужен .NET 6.0 SDK или новее:

1. Перейдите на: https://dotnet.microsoft.com/download
2. Скачайте .NET 6.0 SDK или новее
3. Установите SDK
4. Перезапустите командную строку
5. Выполните: python build_csharp.py

🔧 Альтернативно через winget (Windows 11):
   winget install Microsoft.DotNet.SDK.6

🔧 Альтернативно через Chocolatey:
   choco install dotnet-6.0-sdk

📝 После установки проверьте: dotnet --version
    """)

def main():
    print("🚀 СБОРКА C# МОДУЛЯ ПРОИЗВОДИТЕЛЬНОСТИ")
    print("="*50)
    
    # Проверяем .NET SDK
    if not check_dotnet():
        show_instructions()
        return False
    
    # Собираем модуль
    if not build_csharp_module():
        print("❌ Сборка не удалась")
        return False
    
    # Тестируем модуль
    if not test_csharp_module():
        print("❌ Тестирование не удалось")
        return False
    
    print("\n" + "="*50)
    print("✅ C# МОДУЛЬ ГОТОВ К ИСПОЛЬЗОВАНИЮ!")
    print("="*50)
    print("📦 Файл: PerformanceModule.dll")
    print("🚀 Интеграция: csharp_performance.py")
    print("✅ Статус: Готов для hybrid_app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n⚠️ Приложение будет работать с Python fallback")
        print("💡 C# модуль опционален для дополнительной производительности")
    
    sys.exit(0 if success else 1)
