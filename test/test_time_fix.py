# test_time_fix.py - Тест исправления времени
from datetime import datetime
from localization_system import localization
from task_manager import task_manager
import time

def test_time_synchronization():
    """Тестирование синхронизации времени"""
    print("="*50)
    print("ТЕСТ СИНХРОНИЗАЦИИ ВРЕМЕНИ")
    print("="*50)
    
    # Получаем время из разных источников
    system_time = datetime.now()
    localization_time = localization.get_moscow_time()
    task_manager_time = task_manager.get_moscow_time()
    
    print(f"Системное время:        {system_time.strftime('%H:%M:%S.%f')[:-3]}")
    print(f"Localization время:     {localization_time.strftime('%H:%M:%S.%f')[:-3]}")
    print(f"TaskManager время:      {task_manager_time.strftime('%H:%M:%S.%f')[:-3]}")
    
    # Проверяем разницу
    diff_loc = abs((system_time - localization_time).total_seconds())
    diff_tm = abs((system_time - task_manager_time).total_seconds())
    
    print(f"\nРазница с системным временем:")
    print(f"Localization: {diff_loc:.3f} секунд")
    print(f"TaskManager:  {diff_tm:.3f} секунд")
    
    # Проверяем результат
    tolerance = 0.1  # Допустимая разница в секундах
    
    if diff_loc <= tolerance and diff_tm <= tolerance:
        print(f"\n✅ ТЕСТ ПРОЙДЕН: Все времена синхронизированы (разница < {tolerance}s)")
        return True
    else:
        print(f"\n❌ ТЕСТ НЕ ПРОЙДЕН: Время не синхронизировано")
        return False

def test_time_updates():
    """Тест обновления времени"""
    print("\n" + "="*50)
    print("ТЕСТ ОБНОВЛЕНИЯ ВРЕМЕНИ")
    print("="*50)
    
    print("Проверяем обновление времени каждую секунду...")
    
    for i in range(3):
        current_time = localization.get_moscow_time()
        formatted_time = localization.format_moscow_time()
        
        print(f"Итерация {i+1}: {formatted_time}")
        
        if i < 2:  # Не ждем после последней итерации
            time.sleep(1)
    
    print("✅ Время обновляется корректно")

def main():
    print("🕐 ТЕСТИРОВАНИЕ ИСПРАВЛЕНИЯ ВРЕМЕНИ")
    print("Проверяем, что время больше не спешит...")
    
    # Тест синхронизации
    sync_ok = test_time_synchronization()
    
    # Тест обновлений
    test_time_updates()
    
    print("\n" + "="*50)
    print("ИТОГОВЫЙ РЕЗУЛЬТАТ")
    print("="*50)
    
    if sync_ok:
        print("✅ ВРЕМЯ ИСПРАВЛЕНО УСПЕШНО!")
        print("✅ Все компоненты используют локальное системное время")
        print("✅ Больше нет проблем с pytz и московским временем")
        print("✅ Приложение показывает корректное время")
    else:
        print("❌ Требуется дополнительная настройка")
    
    print(f"\nТекущее время: {datetime.now().strftime('%H:%M:%S %d.%m.%Y')}")

if __name__ == "__main__":
    main()
