// performance_simple.cpp - Упрощенный C++ модуль для демонстрации
#include <iostream>
#include <algorithm>

extern "C" {
    // Простая функция расчета продуктивности
    __declspec(dllexport) double calculate_productivity(int total_blocks, int total_minutes) {
        if (total_blocks == 0) return 0.0;
        
        // Базовый расчет: 8 часов = 100%
        double base_productivity = (static_cast<double>(total_minutes) / 480.0) * 100.0;
        
        // Бонус за количество блоков (лучшее планирование)
        double block_bonus = std::min(20.0, total_blocks * 2.0);
        
        // Итоговая продуктивность
        return std::min(100.0, base_productivity + block_bonus);
    }
    
    // Простая функция бенчмарка
    __declspec(dllexport) double performance_benchmark() {
        // Простой тест производительности
        volatile double result = 0.0;
        for (int i = 0; i < 1000000; ++i) {
            result += i * 0.001;
        }
        return result;
    }
    
    // Функция проверки работоспособности
    __declspec(dllexport) int test_function() {
        return 42; // Магическое число для проверки
    }
}

// Компиляция для Windows:
// g++ -shared -O3 performance_simple.cpp -o performance.dll
// 
// Или с помощью MSVC:
// cl /LD /O2 performance_simple.cpp /Fe:performance.dll
