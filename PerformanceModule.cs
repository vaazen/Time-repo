// PerformanceModule.cs - C# модуль производительности для Windows
using System;
using System.Runtime.InteropServices;

namespace TimeBlockingPerformance
{
    public class PerformanceCalculator
    {
        // Экспорт функции для вызова из Python
        [DllExport("calculate_productivity", CallingConvention = CallingConvention.Cdecl)]
        public static double CalculateProductivity(int totalBlocks, int totalMinutes)
        {
            if (totalBlocks == 0) return 0.0;
            
            // Базовый расчет: 8 часов = 100% продуктивности
            double baseProductivity = (totalMinutes / 480.0) * 100.0;
            
            // Бонус за количество блоков (лучшее планирование)
            double blockBonus = Math.Min(20.0, totalBlocks * 2.0);
            
            // Итоговая продуктивность с учетом эффективности
            double efficiency = CalculateEfficiency(totalBlocks, totalMinutes);
            double finalProductivity = (baseProductivity + blockBonus) * efficiency;
            
            return Math.Min(100.0, finalProductivity);
        }
        
        [DllExport("calculate_efficiency", CallingConvention = CallingConvention.Cdecl)]
        public static double CalculateEfficiency(int totalBlocks, int totalMinutes)
        {
            if (totalBlocks == 0) return 0.0;
            
            // Средняя длительность блока
            double avgBlockDuration = (double)totalMinutes / totalBlocks;
            
            // Оптимальная длительность блока: 45-90 минут
            double efficiency;
            if (avgBlockDuration >= 45 && avgBlockDuration <= 90)
            {
                efficiency = 1.0; // 100% эффективность
            }
            else if (avgBlockDuration < 45)
            {
                // Слишком короткие блоки менее эффективны
                efficiency = avgBlockDuration / 45.0;
            }
            else
            {
                // Слишком длинные блоки тоже менее эффективны
                efficiency = Math.Max(0.5, 90.0 / avgBlockDuration);
            }
            
            return efficiency;
        }
        
        [DllExport("performance_benchmark", CallingConvention = CallingConvention.Cdecl)]
        public static double PerformanceBenchmark()
        {
            // Простой бенчмарк для демонстрации скорости C#
            var startTime = DateTime.Now;
            
            double result = 0.0;
            for (int i = 0; i < 1000000; i++)
            {
                result += Math.Sqrt(i) * Math.Sin(i * 0.001);
            }
            
            var endTime = DateTime.Now;
            var duration = (endTime - startTime).TotalMilliseconds;
            
            return duration;
        }
        
        [DllExport("get_system_info", CallingConvention = CallingConvention.Cdecl)]
        public static IntPtr GetSystemInfo()
        {
            string info = $"C# Module Active|" +
                         $"OS: {Environment.OSVersion}|" +
                         $"CLR: {Environment.Version}|" +
                         $"Processors: {Environment.ProcessorCount}|" +
                         $"Memory: {GC.GetTotalMemory(false) / 1024 / 1024} MB";
            
            return Marshal.StringToHGlobalAnsi(info);
        }
        
        // Освобождение памяти для строк
        [DllExport("free_string", CallingConvention = CallingConvention.Cdecl)]
        public static void FreeString(IntPtr ptr)
        {
            Marshal.FreeHGlobal(ptr);
        }
    }
}

// Атрибут для экспорта функций
public class DllExportAttribute : Attribute
{
    public CallingConvention CallingConvention { get; set; }
    
    public DllExportAttribute(string exportName, CallingConvention callingConvention = CallingConvention.Cdecl)
    {
        CallingConvention = callingConvention;
    }
}
