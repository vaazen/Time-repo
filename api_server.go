// api_server.go - Go микросервис для Time Blocking API
package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "time"
)

// TaskStats представляет статистику задач
type TaskStats struct {
    TotalTasks     int       `json:"total_tasks"`
    CompletedTasks int       `json:"completed_tasks"`
    Efficiency     float64   `json:"efficiency"`
    LastUpdated    time.Time `json:"last_updated"`
}

// Task представляет задачу
type Task struct {
    ID          string    `json:"id"`
    Title       string    `json:"title"`
    Description string    `json:"description"`
    Priority    string    `json:"priority"`
    Status      string    `json:"status"`
    StartTime   time.Time `json:"start_time"`
    EndTime     time.Time `json:"end_time"`
    CreatedAt   time.Time `json:"created_at"`
}

// Глобальное хранилище задач (в реальном проекте - база данных)
var tasks []Task
var taskStats TaskStats

func main() {
    // Инициализация тестовых данных
    initTestData()
    
    // Настройка маршрутов
    http.HandleFunc("/api/tasks", tasksHandler)
    http.HandleFunc("/api/stats", statsHandler)
    http.HandleFunc("/api/health", healthHandler)
    
    // CORS middleware
    http.HandleFunc("/", corsMiddleware)
    
    fmt.Println("🚀 Time Blocking API Server запущен на порту 8080")
    fmt.Println("📊 Доступные эндпоинты:")
    fmt.Println("   GET  /api/tasks  - Получить все задачи")
    fmt.Println("   GET  /api/stats  - Получить статистику")
    fmt.Println("   GET  /api/health - Проверка здоровья сервиса")
    
    log.Fatal(http.ListenAndServe(":8080", nil))
}

func initTestData() {
    // Создаем тестовые задачи
    now := time.Now()
    
    tasks = []Task{
        {
            ID:          "1",
            Title:       "Изучить Go",
            Description: "Освоить основы языка Go для микросервисов",
            Priority:    "high",
            Status:      "completed",
            StartTime:   now.Add(-2 * time.Hour),
            EndTime:     now.Add(-1 * time.Hour),
            CreatedAt:   now.Add(-3 * time.Hour),
        },
        {
            ID:          "2", 
            Title:       "Написать API",
            Description: "Создать REST API для Time Blocking приложения",
            Priority:    "urgent",
            Status:      "in_progress",
            StartTime:   now,
            EndTime:     now.Add(2 * time.Hour),
            CreatedAt:   now.Add(-1 * time.Hour),
        },
        {
            ID:          "3",
            Title:       "Тестирование",
            Description: "Протестировать все эндпоинты API",
            Priority:    "medium",
            Status:      "planned",
            StartTime:   now.Add(2 * time.Hour),
            EndTime:     now.Add(4 * time.Hour),
            CreatedAt:   now,
        },
    }
    
    // Обновляем статистику
    updateStats()
}

func updateStats() {
    completed := 0
    for _, task := range tasks {
        if task.Status == "completed" {
            completed++
        }
    }
    
    efficiency := 0.0
    if len(tasks) > 0 {
        efficiency = float64(completed) / float64(len(tasks)) * 100
    }
    
    taskStats = TaskStats{
        TotalTasks:     len(tasks),
        CompletedTasks: completed,
        Efficiency:     efficiency,
        LastUpdated:    time.Now(),
    }
}

func tasksHandler(w http.ResponseWriter, r *http.Request) {
    setCORSHeaders(w)
    
    switch r.Method {
    case "GET":
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(tasks)
        
    case "POST":
        var newTask Task
        if err := json.NewDecoder(r.Body).Decode(&newTask); err != nil {
            http.Error(w, "Неверный формат JSON", http.StatusBadRequest)
            return
        }
        
        newTask.ID = fmt.Sprintf("%d", len(tasks)+1)
        newTask.CreatedAt = time.Now()
        tasks = append(tasks, newTask)
        updateStats()
        
        w.Header().Set("Content-Type", "application/json")
        w.WriteHeader(http.StatusCreated)
        json.NewEncoder(w).Encode(newTask)
        
    default:
        http.Error(w, "Метод не поддерживается", http.StatusMethodNotAllowed)
    }
}

func statsHandler(w http.ResponseWriter, r *http.Request) {
    setCORSHeaders(w)
    
    if r.Method != "GET" {
        http.Error(w, "Только GET запросы", http.StatusMethodNotAllowed)
        return
    }
    
    updateStats()
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(taskStats)
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
    setCORSHeaders(w)
    
    health := map[string]interface{}{
        "status":    "healthy",
        "timestamp": time.Now(),
        "version":   "1.0.0",
        "service":   "time-blocking-api",
        "uptime":    "running",
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(health)
}

func setCORSHeaders(w http.ResponseWriter) {
    w.Header().Set("Access-Control-Allow-Origin", "*")
    w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
}

func corsMiddleware(w http.ResponseWriter, r *http.Request) {
    setCORSHeaders(w)
    
    if r.Method == "OPTIONS" {
        w.WriteHeader(http.StatusOK)
        return
    }
    
    // Если это не API запрос, возвращаем 404
    if r.URL.Path != "/" {
        http.NotFound(w, r)
        return
    }
    
    // Главная страница
    fmt.Fprintf(w, `
    <html>
    <head>
        <title>Time Blocking API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #1e1e1e; color: white; }
            .endpoint { background: #2d2d2d; padding: 15px; margin: 10px 0; border-radius: 8px; }
            .method { color: #4CAF50; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>🚀 Time Blocking API Server</h1>
        <p>Добро пожаловать в API сервер для управления задачами!</p>
        
        <h2>📊 Доступные эндпоинты:</h2>
        
        <div class="endpoint">
            <span class="method">GET</span> /api/tasks - Получить все задачи
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> /api/tasks - Создать новую задачу
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> /api/stats - Получить статистику
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> /api/health - Проверка здоровья сервиса
        </div>
        
        <p><em>Создано на Go для высокой производительности! 🐹</em></p>
    </body>
    </html>
    `)
}
