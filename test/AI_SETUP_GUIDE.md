# 🤖 Настройка ИИ-помощника

## Проблема: ИИ не отвечает

Если ИИ-помощник отвечает "К сожалению, ИИ-помощник временно недоступен", это означает проблемы с OpenAI API.

## 🔧 Решения

### 1. Проверьте баланс OpenAI API
- Перейдите на https://platform.openai.com/
- Войдите в аккаунт
- Проверьте баланс в разделе "Billing"
- При необходимости пополните баланс

### 2. Получите новый API ключ
1. Зайдите на https://platform.openai.com/api-keys
2. Создайте новый API ключ
3. Скопируйте ключ

### 3. Замените API ключ в коде
Откройте файл `hybrid_app.py` и найдите строку (около строки 742):
```python
openai_key = "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"
```

Замените на ваш новый ключ:
```python
openai_key = "ваш_новый_ключ_здесь"
```

### 4. Альтернативные варианты

#### Вариант A: Использовать другой API
Можете заменить DeepSeek на другой сервис (OpenAI, Claude, etc.)

#### Вариант B: Локальный режим
Добавьте в `ai_assistant.py` режим без ИИ:
```python
# В начале файла добавьте
OFFLINE_MODE = True  # Установите True для работы без ИИ

# В методе _make_request добавьте проверку
def _make_request(self, messages: List[Dict], max_tokens: int = 1000) -> Optional[str]:
    if OFFLINE_MODE:
        return "Работаю в автономном режиме. Общие советы по планированию: используйте технику Помодоро, планируйте не более 3-5 задач в день, делайте регулярные перерывы."
    
    # Остальной код...
```

## 🚀 Быстрое решение

Самый простой способ - установить `OFFLINE_MODE = True` в файле `ai_assistant.py` на строке 15:

```python
class AIAssistant:
    """ИИ-помощник для планирования с использованием DeepSeek API"""
    
    def __init__(self, api_key: str):
        self.offline_mode = True  # Добавьте эту строку
        # ... остальной код
```

И в методе `_make_request` добавьте проверку:
```python
def _make_request(self, messages: List[Dict], max_tokens: int = 1000) -> Optional[str]:
    if hasattr(self, 'offline_mode') and self.offline_mode:
        return "Работаю в автономном режиме. Вот общие советы по планированию..."
    
    # Остальной код API запроса...
```

## 📞 Поддержка

Если проблемы продолжаются:
- 📧 Email: kostybaz@gmail.com
- 💬 Telegram: @vaazen

---

**Приложение будет работать и без ИИ - все остальные функции доступны!** 🎯
