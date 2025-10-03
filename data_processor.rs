// data_processor.rs - Продвинутый анализатор продуктивности на Rust 🦀
use std::env;
use std::fs;
use std::collections::HashMap;
use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc, NaiveDateTime, Local, Timelike};

#[derive(Deserialize, Serialize, Clone, Debug)]
struct TimeBlock {
    id: u32,
    title: String,
    duration: u32,
    created_at: String,
    status: String,
    priority: Option<String>,
    category: Option<String>,
    tags: Option<Vec<String>>,
}

#[derive(Serialize)]
struct ProcessedBlock {
    id: u32,
    title: String,
    duration: u32,
    created_at: String,
    status: String,
    efficiency: f64,
    priority_score: f64,
    optimal_time: String,
    processed_at: String,
    category: String,
    focus_rating: f64,
    energy_level: String,
    improvement_suggestions: Vec<String>,
}

#[derive(Serialize)]
struct ProcessingResult {
    processed_blocks: Vec<ProcessedBlock>,
    total_efficiency: f64,
    optimization_suggestions: Vec<String>,
    performance_metrics: PerformanceMetrics,
    processor: String,
}

#[derive(Serialize)]
struct PerformanceMetrics {
    total_duration: u32,
    average_duration: f64,
    efficiency_distribution: HashMap<String, u32>,
    peak_productivity_hours: Vec<u8>,
    fragmentation_index: f64,
    productivity_score: f64,
    focus_time_percentage: f64,
    category_breakdown: HashMap<String, CategoryStats>,
    weekly_trend: Vec<DayStats>,
    burnout_risk: String,
}

#[derive(Serialize)]
struct CategoryStats {
    total_time: u32,
    efficiency: f64,
    completion_rate: f64,
    count: u32,
}

#[derive(Serialize)]
struct DayStats {
    day: String,
    total_duration: u32,
    efficiency: f64,
    blocks_count: u32,
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() != 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }
    
    let filename = &args[1];
    
    match process_time_blocks(filename) {
        Ok(result) => {
            let json_output = serde_json::to_string_pretty(&result).unwrap();
            println!("{}", json_output);
        }
        Err(e) => {
            eprintln!("Error processing blocks: {}", e);
            std::process::exit(1);
        }
    }
}

fn process_time_blocks(filename: &str) -> Result<ProcessingResult, Box<dyn std::error::Error>> {
    // Читаем входные данные
    let content = fs::read_to_string(filename)?;
    let blocks: Vec<TimeBlock> = serde_json::from_str(&content)?;
    
    if blocks.is_empty() {
        return Ok(ProcessingResult {
            processed_blocks: vec![],
            total_efficiency: 0.0,
            optimization_suggestions: vec!["Добавьте временные блоки для анализа".to_string()],
            performance_metrics: PerformanceMetrics {
                total_duration: 0,
                average_duration: 0.0,
                efficiency_distribution: HashMap::new(),
                peak_productivity_hours: vec![],
                fragmentation_index: 0.0,
                productivity_score: 0.0,
                focus_time_percentage: 0.0,
                category_breakdown: HashMap::new(),
                weekly_trend: vec![],
                burnout_risk: "Низкий".to_string(),
            },
            processor: "rust".to_string(),
        });
    }
    
    // Обрабатываем каждый блок с расширенной аналитикой
    let mut processed_blocks = Vec::new();
    let mut total_efficiency = 0.0;
    
    for block in &blocks {
        let efficiency = calculate_advanced_efficiency(&block);
        let priority_score = calculate_priority_score(&block);
        let optimal_time = suggest_optimal_time(&block);
        let category = determine_category(&block);
        let focus_rating = calculate_focus_rating(&block);
        let energy_level = determine_energy_level(&block);
        let improvement_suggestions = generate_block_suggestions(&block);
        
        processed_blocks.push(ProcessedBlock {
            id: block.id,
            title: block.title.clone(),
            duration: block.duration,
            created_at: block.created_at.clone(),
            status: block.status.clone(),
            efficiency,
            priority_score,
            optimal_time,
            processed_at: Utc::now().to_rfc3339(),
            category,
            focus_rating,
            energy_level,
            improvement_suggestions,
        });
        
        total_efficiency += efficiency;
    }
    
    total_efficiency /= blocks.len() as f64;
    
    // Генерируем метрики производительности
    let performance_metrics = generate_advanced_performance_metrics(&blocks);
    
    // Генерируем рекомендации по оптимизации
    let optimization_suggestions = generate_optimization_suggestions(&blocks, &performance_metrics);
    
    Ok(ProcessingResult {
        processed_blocks,
        total_efficiency,
        optimization_suggestions,
        performance_metrics,
        processor: "rust".to_string(),
    })
}

fn calculate_advanced_efficiency(block: &TimeBlock) -> f64 {
    // Алгоритм расчета эффективности блока
    let base_efficiency = match block.duration {
        0..=30 => 60.0,      // Короткие блоки менее эффективны
        31..=90 => 85.0,     // Оптимальная длительность
        91..=180 => 95.0,    // Хорошая длительность для глубокой работы
        181..=300 => 80.0,   // Длинные блоки могут быть менее эффективны
        _ => 60.0,           // Очень длинные блоки
    };
    
    // Бонус за статус
    let status_multiplier = match block.status.as_str() {
        "completed" => 1.2,
        "active" => 1.0,
        "planned" => 0.8,
        _ => 0.9,
    };
    
    // Учитываем время создания (недавние блоки более актуальны)
    let time_bonus = 1.0; // Упрощенно, в реальности бы парсили дату
    
    (base_efficiency * status_multiplier * time_bonus).min(100.0)
}

fn calculate_priority_score(block: &TimeBlock) -> f64 {
    // Расчет приоритета на основе различных факторов
    let duration_score = (block.duration as f64 / 120.0).min(1.0) * 40.0; // До 40 баллов за длительность
    
    let title_score = if block.title.to_lowercase().contains("важн") || 
                         block.title.to_lowercase().contains("срочн") {
        30.0
    } else if block.title.to_lowercase().contains("встреча") ||
              block.title.to_lowercase().contains("звонок") {
        25.0
    } else {
        20.0
    };
    
    let status_score = match block.status.as_str() {
        "active" => 30.0,
        "planned" => 20.0,
        "completed" => 10.0,
        _ => 15.0,
    };
    
    duration_score + title_score + status_score
}

fn suggest_optimal_time(block: &TimeBlock) -> String {
    // Предлагаем оптимальное время для выполнения задачи
    match block.duration {
        0..=60 => "09:00-10:00 (утренняя концентрация)".to_string(),
        61..=120 => "10:00-12:00 (пик продуктивности)".to_string(),
        121..=180 => "14:00-17:00 (послеобеденная работа)".to_string(),
        _ => "09:00-12:00 (утренний блок)".to_string(),
    }
}

fn generate_performance_metrics(blocks: &[TimeBlock]) -> PerformanceMetrics {
    let total_duration: u32 = blocks.iter().map(|b| b.duration).sum();
    let average_duration = total_duration as f64 / blocks.len() as f64;
    
    // Распределение эффективности
    let mut efficiency_distribution = HashMap::new();
    for block in blocks {
        let efficiency = calculate_efficiency(block);
        let category = match efficiency as u32 {
            0..=60 => "low",
            61..=80 => "medium",
            81..=95 => "high",
            _ => "excellent",
        };
        *efficiency_distribution.entry(category.to_string()).or_insert(0) += 1;
    }
    
    // Пиковые часы продуктивности (упрощенно)
    let peak_productivity_hours = vec![9, 10, 11, 14, 15];
    
    // Индекс фрагментации (много коротких блоков = высокая фрагментация)
    let short_blocks = blocks.iter().filter(|b| b.duration < 60).count();
    let fragmentation_index = (short_blocks as f64 / blocks.len() as f64) * 100.0;
    
    PerformanceMetrics {
        total_duration,
        average_duration,
        efficiency_distribution,
        peak_productivity_hours,
        fragmentation_index,
    }
}

fn generate_optimization_suggestions(blocks: &[TimeBlock], metrics: &PerformanceMetrics) -> Vec<String> {
    let mut suggestions = Vec::new();
    
    // Анализ фрагментации
    if metrics.fragmentation_index > 50.0 {
        suggestions.push("🔄 Слишком много коротких блоков. Попробуйте объединить похожие задачи.".to_string());
    }
    
    // Анализ средней длительности
    if metrics.average_duration < 45.0 {
        suggestions.push("⏰ Увеличьте длительность блоков для лучшей концентрации (рекомендуется 60-90 мин).".to_string());
    } else if metrics.average_duration > 180.0 {
        suggestions.push("✂️ Разбейте длинные блоки на более короткие для лучшего фокуса.".to_string());
    }
    
    // Анализ общего времени
    if metrics.total_duration < 240 {
        suggestions.push("📈 Увеличьте общее время планирования для повышения продуктивности.".to_string());
    }
    
    // Анализ статусов
    let completed_count = blocks.iter().filter(|b| b.status == "completed").count();
    let completion_rate = (completed_count as f64 / blocks.len() as f64) * 100.0;
    
    if completion_rate < 70.0 {
        suggestions.push("✅ Низкий процент выполнения задач. Планируйте более реалистично.".to_string());
    }
    
    // Рекомендации по времени
    suggestions.push("🌅 Планируйте сложные задачи на утренние часы (9:00-12:00).".to_string());
    suggestions.push("🍽️ Используйте послеобеденное время для рутинных задач.".to_string());
    
    if suggestions.is_empty() {
        suggestions.push("🎉 Отличное планирование! Продолжайте в том же духе.".to_string());
    }
    
    suggestions
}

// Новые функции для расширенного анализа
fn determine_category(block: &TimeBlock) -> String {
    if let Some(category) = &block.category {
        return category.clone();
    }
    
    let title_lower = block.title.to_lowercase();
    match title_lower {
        t if t.contains("встреча") || t.contains("звонок") || t.contains("совещание") => "Коммуникация".to_string(),
        t if t.contains("код") || t.contains("программ") || t.contains("разработка") => "Разработка".to_string(),
        t if t.contains("изучен") || t.contains("обучен") || t.contains("курс") => "Обучение".to_string(),
        t if t.contains("планир") || t.contains("анализ") || t.contains("стратег") => "Планирование".to_string(),
        t if t.contains("тест") || t.contains("отладка") || t.contains("исправл") => "Тестирование".to_string(),
        t if t.contains("документ") || t.contains("отчет") || t.contains("описан") => "Документация".to_string(),
        _ => "Общие задачи".to_string(),
    }
}

fn calculate_focus_rating(block: &TimeBlock) -> f64 {
    // Рейтинг фокуса на основе длительности и типа задачи
    let duration_rating = match block.duration {
        0..=15 => 3.0,      // Очень низкий фокус
        16..=45 => 5.0,     // Низкий фокус
        46..=90 => 8.0,     // Хороший фокус
        91..=120 => 9.5,    // Отличный фокус
        121..=180 => 9.0,   // Очень хороший фокус
        _ => 7.0,           // Длинные блоки могут терять фокус
    };
    
    // Бонус за тип задачи
    let title_lower = block.title.to_lowercase();
    let task_bonus = if title_lower.contains("глубок") || title_lower.contains("сложн") {
        1.0
    } else if title_lower.contains("рутин") || title_lower.contains("простой") {
        -0.5
    } else {
        0.0
    };
    
    (duration_rating + task_bonus).max(1.0).min(10.0)
}

fn determine_energy_level(block: &TimeBlock) -> String {
    // Определяем уровень энергии на основе времени и длительности
    match block.duration {
        0..=30 => "Низкая".to_string(),
        31..=90 => "Средняя".to_string(),
        91..=180 => "Высокая".to_string(),
        _ => "Очень высокая".to_string(),
    }
}

fn generate_block_suggestions(block: &TimeBlock) -> Vec<String> {
    let mut suggestions = Vec::new();
    
    // Анализ длительности
    match block.duration {
        0..=15 => suggestions.push("⏰ Слишком короткий блок. Увеличьте до 25-30 минут.".to_string()),
        16..=25 => suggestions.push("🍅 Отлично для техники Pomodoro!".to_string()),
        46..=90 => suggestions.push("✨ Идеальная длительность для глубокой работы.".to_string()),
        181.. => suggestions.push("✂️ Рассмотрите разбиение на более короткие блоки.".to_string()),
        _ => {}
    }
    
    // Анализ статуса
    if block.status == "planned" {
        suggestions.push("📋 Не забудьте начать выполнение в запланированное время.".to_string());
    } else if block.status == "completed" {
        suggestions.push("🎉 Отлично! Задача выполнена.".to_string());
    }
    
    // Анализ приоритета
    if let Some(priority) = &block.priority {
        match priority.as_str() {
            "urgent" => suggestions.push("🚨 Высокий приоритет - выполните в первую очередь.".to_string()),
            "high" => suggestions.push("⚡ Важная задача - запланируйте на утро.".to_string()),
            _ => {}
        }
    }
    
    suggestions
}

// Обновленная функция генерации метрик
fn generate_advanced_performance_metrics(blocks: &[TimeBlock]) -> PerformanceMetrics {
    let total_duration: u32 = blocks.iter().map(|b| b.duration).sum();
    let average_duration = total_duration as f64 / blocks.len() as f64;
    
    // Распределение эффективности
    let mut efficiency_distribution = HashMap::new();
    let mut total_efficiency = 0.0;
    
    for block in blocks {
        let efficiency = calculate_advanced_efficiency(block);
        total_efficiency += efficiency;
        
        let category = match efficiency as u32 {
            0..=60 => "Низкая",
            61..=80 => "Средняя", 
            81..=95 => "Высокая",
            _ => "Отличная",
        };
        *efficiency_distribution.entry(category.to_string()).or_insert(0) += 1;
    }
    
    let productivity_score = total_efficiency / blocks.len() as f64;
    
    // Процент времени в фокусе (блоки > 45 минут)
    let focus_blocks = blocks.iter().filter(|b| b.duration >= 45).count();
    let focus_time_percentage = (focus_blocks as f64 / blocks.len() as f64) * 100.0;
    
    // Разбивка по категориям
    let mut category_breakdown = HashMap::new();
    for block in blocks {
        let category = determine_category(block);
        let stats = category_breakdown.entry(category).or_insert(CategoryStats {
            total_time: 0,
            efficiency: 0.0,
            completion_rate: 0.0,
            count: 0,
        });
        
        stats.total_time += block.duration;
        stats.efficiency += calculate_advanced_efficiency(block);
        stats.count += 1;
        if block.status == "completed" {
            stats.completion_rate += 1.0;
        }
    }
    
    // Нормализуем статистики по категориям
    for stats in category_breakdown.values_mut() {
        stats.efficiency /= stats.count as f64;
        stats.completion_rate = (stats.completion_rate / stats.count as f64) * 100.0;
    }
    
    // Пиковые часы продуктивности
    let peak_productivity_hours = vec![9, 10, 11, 14, 15, 16];
    
    // Индекс фрагментации
    let short_blocks = blocks.iter().filter(|b| b.duration < 45).count();
    let fragmentation_index = (short_blocks as f64 / blocks.len() as f64) * 100.0;
    
    // Недельный тренд (упрощенно)
    let weekly_trend = vec![
        DayStats { day: "Понедельник".to_string(), total_duration: total_duration / 7, efficiency: productivity_score, blocks_count: blocks.len() as u32 / 7 },
        DayStats { day: "Вторник".to_string(), total_duration: total_duration / 7, efficiency: productivity_score * 1.1, blocks_count: blocks.len() as u32 / 7 },
        DayStats { day: "Среда".to_string(), total_duration: total_duration / 7, efficiency: productivity_score * 1.05, blocks_count: blocks.len() as u32 / 7 },
    ];
    
    // Риск выгорания
    let burnout_risk = if total_duration > 600 && fragmentation_index > 60.0 {
        "Высокий".to_string()
    } else if total_duration > 400 {
        "Средний".to_string()
    } else {
        "Низкий".to_string()
    };
    
    PerformanceMetrics {
        total_duration,
        average_duration,
        efficiency_distribution,
        peak_productivity_hours,
        fragmentation_index,
        productivity_score,
        focus_time_percentage,
        category_breakdown,
        weekly_trend,
        burnout_risk,
    }
}

// Добавляем зависимости в Cargo.toml:
/*
[dependencies]
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
chrono = { version = "0.4", features = ["serde"] }
*/

// Компиляция:
// cargo build --release
// Исполняемый файл будет в target/release/data_processor.exe
