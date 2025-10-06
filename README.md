# Time Blocking - Приложение для планирования времени

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://pypi.org/project/PyQt5/)

**Time Blocking** - это современное гибридное приложение для управления временем и задачами с поддержкой искусственного интеллекта и интеграцией с популярными сервисами.

## 📋 Содержание

- [Особенности](#особенности)
- [Установка](#установка)
- [Быстрый старт](#быстрый-старт)
- [Архитектура](#архитектура)
- [API и модули](#api-и-модули)
- [Конфигурация](#конфигурация)
- [Интеграции](#интеграции)
- [Разработка](#разработка)
- [Устранение неполадок](#устранение-неполадок)
- [Лицензия](#лицензия)

## 🚀 Особенности

### Основной функционал
- **Time Blocking** - планирование времени блоками
- **Управление задачами** - создание, редактирование, приоритизация
- **Аналитика** - детальная статистика продуктивности
- **Уведомления** - умные напоминания о задачах
- **Экспорт данных** - в различные форматы (JSON, Excel, PDF)

### ИИ-Помощник (v5.0)
- **Анализ задач** - умная приоритизация с помощью DeepSeek API
- **Автопланирование** - создание оптимального расписания
- **Персональные инсайты** - рекомендации на основе данных
- **Чат-консультант** - интерактивные советы по планированию

### Интеграции
- **Slack** - уведомления в каналы и DM
- **Trello** - синхронизация с досками проектов
- **Notion** - создание страниц и записей
- **Dropbox** - облачная синхронизация данных

### Технические особенности
- **Гибридная архитектура** - Python, C#, Rust, Go
- **Модульная структура** - легкое расширение функционала
- **Многоязычность** - поддержка локализации
- **Кроссплатформенность** - Windows, macOS, Linux

## 📦 Установка

### Системные требования
- Python 3.7+
- PyQt5 5.15+
- 4 ГБ ОЗУ (рекомендуется 8 ГБ)
- 500 МБ свободного места на диске

### Установка зависимостей

```bash
# Клонирование репозитория
git clone https://github.com/vaazen/Time.git
cd Time

# Установка Python зависимостей
pip install -r requirements.txt

# Для разработчиков (дополнительные инструменты)
pip install -r requirements-dev.txt
```

### Сборка нативных модулей (опционально)

```bash
# Сборка C# модуля производительности
python build_csharp.py

# Сборка Rust модуля обработки данных
cargo build --release

# Сборка Go API сервера
go build -o bin/api_server api_server.go
```

## 🏃‍♂️ Быстрый старт

### Базовый запуск

```bash
# Запуск основного приложения
python hybrid_app.py
```

### Первоначальная настройка

1. **Выбор языка интерфейса**
   - При первом запуске выберите предпочитаемый язык
   - Поддерживаются: русский, английский, испанский, французский

2. **Настройка ИИ-помощника**
   - Перейдите во вкладку "ИИ-Помощник"
   - При необходимости настройте API ключ DeepSeek

3. **Подключение интеграций**
   - Откройте вкладку "Интеграции"
   - Настройте нужные сервисы (Slack, Trello, Notion)

### Создание первой задачи

```python
# Пример создания задачи через API
from task_manager import task_manager, Task, TaskPriority

task = Task(
    title="Изучить документацию",
    description="Прочитать README и настроить приложение",
    priority=TaskPriority.HIGH,
    duration_minutes=60
)

task_manager.add_task(task)
```

## 🏗️ Архитектура

### Структура проекта

```
Time/
├── hybrid_app.py              # Главное приложение
├── core/                      # Основные модули
│   ├── task_manager.py        # Управление задачами
│   ├── data_manager.py        # Управление данными
│   └── localization_system.py # Система локализации
├── ai_assistant.py            # ИИ-помощник
├── integrations_manager.py    # Менеджер интеграций
├── advanced_analytics.py     # Расширенная аналитика
├── smart_notifications.py    # Умные уведомления
├── cloud_sync.py             # Облачная синхронизация
├── performance_optimizer.py  # Оптимизатор производительности
├── models/                   # Модели данных
├── services/                 # Внешние сервисы
├── presenters/              # Презентеры (MVP)
├── translations/            # Файлы переводов
└── test/                    # Тесты
```

### Паттерны проектирования

- **MVP (Model-View-Presenter)** - разделение логики и UI
- **Observer** - система уведомлений
- **Factory** - создание объектов задач
- **Singleton** - менеджеры ресурсов
- **Strategy** - различные алгоритмы планирования

### Многоязычная архитектура

```mermaid
graph TD
    A[Python - UI & Logic] --> B[C# - Performance Module]
    A --> C[Rust - Data Processing]
    A --> D[Go - API Server]
    A --> E[JavaScript - Dashboard]
    
    B --> F[Native Performance]
    C --> G[Fast Data Processing]
    D --> H[HTTP API]
    E --> I[Interactive Charts]
```

## 📚 API и модули

### TaskManager API

```python
from task_manager import task_manager

# Создание задачи
task = task_manager.create_task(
    title="Название задачи",
    description="Описание",
    priority=TaskPriority.HIGH,
    duration_minutes=60
)

# Получение задач
tasks = task_manager.get_tasks()
active_tasks = task_manager.get_active_tasks()

# Обновление статуса
task_manager.update_task_status(task_id, TaskStatus.COMPLETED)
```

### AIAssistant API

```python
from ai_assistant import AIAssistant

ai = AIAssistant()

# Анализ задач
analysis = ai.analyze_tasks(tasks)

# Создание расписания
schedule = ai.create_smart_schedule(tasks, preferences)

# Получение инсайтов
insights = ai.get_productivity_insights(user_data)
```

### IntegrationsManager API

```python
from integrations_manager import IntegrationsManager

integrations = IntegrationsManager()

# Настройка Slack
integrations.setup_slack(webhook_url="https://hooks.slack.com/...")

# Отправка уведомления
integrations.send_notification("slack", "Задача выполнена!")

# Синхронизация с Trello
integrations.sync_with_trello(board_id="board123")
```

### AdvancedAnalytics API

```python
from advanced_analytics import get_advanced_analytics_widget

analytics = get_advanced_analytics_widget()

# Получение статистики
stats = analytics.get_productivity_stats()
trends = analytics.get_productivity_trends()

# Генерация отчетов
report = analytics.generate_weekly_report()
```

## ⚙️ Конфигурация

### Файл конфигурации (config.json)

```json
{
  "ui": {
    "language": "ru",
    "theme": "dark",
    "animations_enabled": true
  },
  "ai": {
    "provider": "deepseek",
    "api_key": "your_api_key_here",
    "model": "deepseek-chat"
  },
  "integrations": {
    "slack": {
      "enabled": true,
      "webhook_url": "https://hooks.slack.com/..."
    },
    "trello": {
      "enabled": false,
      "api_key": "",
      "token": ""
    }
  },
  "data": {
    "backup_enabled": true,
    "cloud_sync": true,
    "export_format": "json"
  }
}
```

### Переменные окружения

```bash
# ИИ настройки
export DEEPSEEK_API_KEY="your_deepseek_key"
export AI_MODEL="deepseek-chat"

# Интеграции
export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."
export TRELLO_API_KEY="your_trello_key"
export NOTION_TOKEN="your_notion_token"

# Облачная синхронизация
export DROPBOX_ACCESS_TOKEN="your_dropbox_token"
```

## 🔗 Интеграции

### Slack

```python
# Настройка через Webhook
integrations.setup_slack(
    webhook_url="https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
)

# Настройка через Bot Token
integrations.setup_slack(
    bot_token="xoxb-000000000000-000000000000-XXXXXXXXXXXXXXXXXXXXXXXX",
    channel="#general"
)
```

### Trello

```python
# Получение API ключей: https://trello.com/app-key
integrations.setup_trello(
    api_key="your_trello_api_key",
    token="your_trello_token",
    board_id="your_board_id"
)
```

### Notion

```python
# Создание интеграции: https://notion.so/my-integrations
integrations.setup_notion(
    token="secret_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    database_id="your_database_id"
)
```

## 🛠️ Разработка

### Настройка среды разработки

```bash
# Установка инструментов разработки
pip install -r requirements-dev.txt

# Настройка pre-commit хуков
pre-commit install

# Запуск тестов
python -m pytest test/

# Проверка кода
flake8 .
black .
mypy .
```

### Создание нового модуля

```python
# Шаблон модуля
class NewModule:
    def __init__(self):
        self.name = "NewModule"
    
    def initialize(self):
        """Инициализация модуля"""
        pass
    
    def cleanup(self):
        """Очистка ресурсов"""
        pass

# Регистрация в hybrid_app.py
from new_module import NewModule
new_module = NewModule()
```

### Добавление переводов

```python
# В файле translations/ru.json
{
    "new_feature": "Новая функция",
    "new_feature_description": "Описание новой функции"
}

# Использование в коде
from localization_system import _
label_text = _("new_feature")
```

## 🔧 Устранение неполадок

### Частые проблемы

#### PyQtWebEngine не найден
```bash
# Решение для Windows
pip install PyQtWebEngine

# Решение для Linux
sudo apt-get install python3-pyqt5.qtwebengine

# Решение для macOS
brew install pyqt5
```

#### Ошибки ИИ-модуля
```python
# Проверка доступности API
from ai_assistant import AIAssistant
ai = AIAssistant()
if ai.test_connection():
    print("ИИ доступен")
else:
    print("Проверьте API ключ и интернет соединение")
```

#### Проблемы с интеграциями
```python
# Тестирование интеграций
from integrations_manager import IntegrationsManager
integrations = IntegrationsManager()
status = integrations.test_all_integrations()
print(status)
```

### Логирование

```python
import logging

# Включение подробного логирования
logging.basicConfig(level=logging.DEBUG)

# Просмотр логов
tail -f logs/time_blocking.log
```

### Сбор диагностической информации

```bash
# Запуск диагностики
python -c "
import sys
print('Python:', sys.version)
import PyQt5.Qt
print('PyQt5:', PyQt5.Qt.PYQT_VERSION_STR)
"
```

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта! См. [CONTRIBUTING.md](CONTRIBUTING.md) для получения подробной информации.

## 📞 Поддержка

- **Email**: kostybaz@gmail.com
- **Telegram**: @vaazen
- **Issues**: [GitHub Issues](https://github.com/vaazen/Time/issues)
- **Discussions**: [GitHub Discussions](https://github.com/vaazen/Time/discussions)

---

*Разработано с ❤️ для повышения продуктивности*
