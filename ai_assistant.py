"""
🤖 ИИ-помощник для планирования задач
Использует DeepSeek API для интеллектуального анализа и планирования
"""

import requests
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import tkinter as tk
from tkinter import messagebox
import threading
import time

class AIAssistant:
    """ИИ-помощник для планирования с использованием OpenAI API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        # Изменяем на OpenAI API
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.logger = logging.getLogger(__name__)
        self.offline_mode = False  # Можно установить True для работы без API
        self.api_error_count = 0  # Счетчик ошибок API
        
    def reset_api_status(self):
        """Сброс статуса API для повторной попытки подключения"""
        self.offline_mode = False
        self.api_error_count = 0
        print("API статус сброшен. Попробую подключиться к OpenAI...")
        
    def _make_request(self, messages: List[Dict], max_tokens: int = 1000) -> Optional[str]:
        """Выполнить запрос к OpenAI API"""
        
        # Автоматический переход в офлайн режим после 3 ошибок
        if self.api_error_count >= 3:
            self.offline_mode = True
        
        # Офлайн режим - возвращаем заготовленные ответы
        if self.offline_mode:
            return self._get_offline_response(messages)
        
        try:
            payload = {
                "model": "gpt-3.5-turbo",  # Изменяем на OpenAI модель
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "stream": False
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                self.api_error_count = 0  # Сбрасываем счетчик при успехе
                return result["choices"][0]["message"]["content"]
            else:
                self.logger.error(f"API Error: {response.status_code} - {response.text}")
                self.api_error_count += 1
                return None
                
        except Exception as e:
            self.logger.error(f"Request failed: {str(e)}")
            self.api_error_count += 1
            return None
    
    def _get_offline_response(self, messages: List[Dict]) -> str:
        """Получить ответ в офлайн режиме"""
        user_message = ""
        for msg in messages:
            if msg.get("role") == "user":
                user_message = msg.get("content", "").lower()
                break
        
        # Простые ответы на основе ключевых слов
        if any(word in user_message for word in ["привет", "hello", "здравствуй"]):
            return "Привет! Я ваш помощник по планированию. Работаю в автономном режиме, но готов помочь с базовыми советами!"
        
        elif any(word in user_message for word in ["задач", "планирование", "расписание"]):
            return """Вот основные принципы эффективного планирования:

• Правило 3: планируйте максимум 3 важные задачи на день
• Техника Помодоро: 25 минут работы + 5 минут отдыха
• Начинайте с самых сложных задач утром
• Группируйте похожие задачи вместе
• Оставляйте 25% времени на непредвиденные дела"""
        
        elif any(word in user_message for word in ["продуктивность", "эффективность"]):
            return """Советы для повышения продуктивности:

• Уберите отвлекающие факторы (телефон, соцсети)
• Работайте в одной задаче за раз
• Делайте регулярные перерывы каждые 90 минут
• Планируйте день с вечера
• Отслеживайте время выполнения задач"""
        
        elif any(word in user_message for word in ["мотивация", "лень"]):
            return """Как побороть прокрастинацию:

• Разбивайте большие задачи на маленькие шаги
• Используйте правило 2 минут: если задача займет меньше 2 минут - делайте сразу
• Награждайте себя за выполненные задачи
• Найдите свое продуктивное время дня
• Создайте ритуалы начала работы"""
        
        else:
            return """Работаю в автономном режиме. Могу дать общие советы по:

• Планированию задач и времени
• Повышению продуктивности
• Борьбе с прокрастинацией
• Организации рабочего дня
• Техникам концентрации

Задавайте конкретные вопросы, и я постараюсь помочь!"""
    
    def analyze_tasks(self, tasks: List[Dict]) -> Dict[str, Any]:
        """Анализ задач и предоставление рекомендаций"""
        
        # Подготовка данных о задачах для анализа
        task_summary = []
        for task in tasks:
            task_info = {
                "название": task.get("title", ""),
                "описание": task.get("description", ""),
                "приоритет": task.get("priority", "medium"),
                "время_создания": task.get("created_at", ""),
                "дедлайн": task.get("deadline", ""),
                "статус": task.get("status", "pending"),
                "категория": task.get("category", "")
            }
            task_summary.append(task_info)
        
        messages = [
            {
                "role": "system",
                "content": """Ты - эксперт по продуктивности и планированию задач. 
                Анализируй задачи пользователя и предоставляй практические рекомендации на русском языке.
                Отвечай в формате JSON со следующими полями:
                - "приоритизация": список задач в порядке важности
                - "временные_блоки": рекомендации по распределению времени
                - "оптимизация": предложения по улучшению планирования
                - "предупреждения": потенциальные проблемы или конфликты
                - "мотивация": мотивирующее сообщение"""
            },
            {
                "role": "user",
                "content": f"Проанализируй мои задачи и дай рекомендации: {json.dumps(task_summary, ensure_ascii=False, indent=2)}"
            }
        ]
        
        response = self._make_request(messages, max_tokens=1500)
        
        if response:
            try:
                # Попытка парсинга JSON ответа
                analysis = json.loads(response)
                return analysis
            except json.JSONDecodeError:
                # Если не JSON, возвращаем текстовый анализ
                return {
                    "анализ": response,
                    "статус": "текстовый_ответ"
                }
        
        return {
            "ошибка": "ИИ-помощник недоступен",
            "причина": "Проблемы с OpenAI API (возможно, недостаточный баланс или неверный ключ)",
            "рекомендации": [
                "Проверьте баланс OpenAI API на platform.openai.com",
                "Убедитесь в правильности API ключа",
                "Проверьте интернет-соединение",
                "Попробуйте повторить запрос через несколько минут"
            ]
        }
    
    def suggest_time_blocks(self, tasks: List[Dict], available_hours: int = 8) -> List[Dict]:
        """Предложить оптимальное распределение времени для задач"""
        
        messages = [
            {
                "role": "system",
                "content": f"""Ты - эксперт по тайм-менеджменту. Создай оптимальное расписание для задач.
                У пользователя есть {available_hours} часов для работы.
                Отвечай в формате JSON со списком временных блоков:
                [{{"задача": "название", "время_начала": "HH:MM", "продолжительность": "минуты", "обоснование": "почему именно это время"}}]
                Учитывай приоритеты, сложность задач и естественные ритмы продуктивности."""
            },
            {
                "role": "user",
                "content": f"Создай расписание для задач: {json.dumps([{'название': t.get('title', ''), 'приоритет': t.get('priority', 'medium'), 'описание': t.get('description', '')} for t in tasks], ensure_ascii=False)}"
            }
        ]
        
        response = self._make_request(messages, max_tokens=1200)
        
        if response:
            try:
                schedule = json.loads(response)
                return schedule if isinstance(schedule, list) else []
            except json.JSONDecodeError:
                return []
        
        return []
    
    def generate_smart_reminders(self, task: Dict) -> List[str]:
        """Генерация умных напоминаний для задачи"""
        
        messages = [
            {
                "role": "system",
                "content": """Создай список умных напоминаний для задачи.
                Напоминания должны быть мотивирующими, конкретными и полезными.
                Отвечай списком строк на русском языке (максимум 5 напоминаний)."""
            },
            {
                "role": "user",
                "content": f"Создай напоминания для задачи: {task.get('title', '')} - {task.get('description', '')}"
            }
        ]
        
        response = self._make_request(messages, max_tokens=500)
        
        if response:
            # Разбиваем ответ на строки и очищаем
            reminders = [line.strip() for line in response.split('\n') if line.strip()]
            return reminders[:5]  # Максимум 5 напоминаний
        
        return ["Не забудьте выполнить эту задачу!"]
    
    def productivity_insights(self, completed_tasks: List[Dict], productivity_data: Dict) -> Dict:
        """Анализ продуктивности и предоставление инсайтов"""
        
        messages = [
            {
                "role": "system",
                "content": """Анализируй данные о продуктивности и предоставляй инсайты.
                Отвечай в формате JSON:
                {
                    "основные_паттерны": "описание паттернов работы",
                    "рекомендации": ["список рекомендаций"],
                    "сильные_стороны": ["что работает хорошо"],
                    "области_улучшения": ["что можно улучшить"],
                    "прогноз": "прогноз на следующий период"
                }"""
            },
            {
                "role": "user",
                "content": f"""Проанализируй мою продуктивность:
                Завершенные задачи: {len(completed_tasks)}
                Данные продуктивности: {json.dumps(productivity_data, ensure_ascii=False)}
                Последние задачи: {json.dumps([{'название': t.get('title', ''), 'время_выполнения': t.get('completion_time', '')} for t in completed_tasks[-10:]], ensure_ascii=False)}"""
            }
        ]
        
        response = self._make_request(messages, max_tokens=1000)
        
        if response:
            try:
                insights = json.loads(response)
                return insights
            except json.JSONDecodeError:
                return {"анализ": response}
        
        return {"ошибка": "Не удалось получить анализ продуктивности"}
    
    def suggest_break_schedule(self, work_duration: int) -> List[Dict]:
        """Предложить оптимальное расписание перерывов"""
        
        messages = [
            {
                "role": "system",
                "content": f"""Создай оптимальное расписание перерывов для {work_duration} часов работы.
                Используй научные данные о продуктивности (техника Помодоро, правило 52/17 и др.).
                Отвечай в формате JSON со списком перерывов:
                [{{"время": "HH:MM", "тип": "короткий/длинный", "продолжительность": "минуты", "активность": "что делать"}}]"""
            },
            {
                "role": "user",
                "content": f"Создай расписание перерывов для {work_duration} часов работы"
            }
        ]
        
        response = self._make_request(messages, max_tokens=800)
        
        if response:
            try:
                breaks = json.loads(response)
                return breaks if isinstance(breaks, list) else []
            except json.JSONDecodeError:
                return []
        
        return []
    
    def chat_with_assistant(self, user_message: str, context: Dict = None) -> str:
        """Чат с ИИ-помощником для получения советов по планированию"""
        
        system_message = """Ты - персональный ИИ-помощник по продуктивности и планированию.
        Отвечай на русском языке, давай практические советы, будь дружелюбным и мотивирующим.
        Помогай с планированием задач, тайм-менеджментом, мотивацией и организацией работы."""
        
        messages = [{"role": "system", "content": system_message}]
        
        # Добавляем контекст если есть
        if context:
            context_message = f"Контекст пользователя: {json.dumps(context, ensure_ascii=False)}"
            messages.append({"role": "system", "content": context_message})
        
        messages.append({"role": "user", "content": user_message})
        
        response = self._make_request(messages, max_tokens=800)
        
        if response:
            return response
        else:
            # Более информативное сообщение об ошибке
            return """К сожалению, ИИ-помощник временно недоступен. 
            
Возможные причины:
• Недостаточный баланс на OpenAI API
• Неверный API ключ
• Проблемы с интернет-соединением  
• Превышен лимит запросов

Попробуйте:
1. Проверить баланс на platform.openai.com
2. Убедиться в правильности API ключа
3. Проверить интернет-соединение
4. Повторить запрос через несколько минут

Пока что могу предложить общие советы по планированию:
• Начинайте день с самых важных задач
• Используйте технику Помодоро (25 мин работы + 5 мин отдыха)
• Планируйте не более 3-5 ключевых задач на день
• Делайте регулярные перерывы для поддержания концентрации"""


class AIAssistantUI:
    """Интерфейс для ИИ-помощника"""
    
    def __init__(self, parent, ai_assistant: AIAssistant):
        self.parent = parent
        self.ai_assistant = ai_assistant
        self.chat_window = None
        
    def create_ai_tab(self, notebook):
        """Создать вкладку ИИ-помощника"""
        ai_frame = tk.Frame(notebook)
        notebook.add(ai_frame, text="🤖 ИИ-Помощник")
        
        # Заголовок
        title_label = tk.Label(ai_frame, text="🤖 ИИ-Помощник для планирования", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Кнопки функций
        buttons_frame = tk.Frame(ai_frame)
        buttons_frame.pack(pady=10)
        
        tk.Button(buttons_frame, text="📊 Анализ задач", 
                 command=self.analyze_current_tasks,
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="⏰ Умное планирование", 
                 command=self.smart_scheduling,
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="💡 Инсайты продуктивности", 
                 command=self.show_productivity_insights,
                 bg="#FF9800", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="💬 Чат с ИИ", 
                 command=self.open_chat_window,
                 bg="#9C27B0", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Область для отображения результатов
        self.results_text = tk.Text(ai_frame, height=20, width=80, wrap=tk.WORD)
        self.results_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Скроллбар
        scrollbar = tk.Scrollbar(ai_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)
        
        return ai_frame
    
    def analyze_current_tasks(self):
        """Анализ текущих задач"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "🔄 Анализирую ваши задачи...\n\n")
        self.parent.update()
        
        def analyze():
            try:
                # Получаем задачи из основного приложения
                tasks = getattr(self.parent, 'tasks', [])
                if not tasks:
                    self.results_text.insert(tk.END, "❌ Нет задач для анализа. Создайте несколько задач сначала.\n")
                    return
                
                analysis = self.ai_assistant.analyze_tasks(tasks)
                
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "🤖 Анализ ваших задач:\n\n")
                
                for key, value in analysis.items():
                    self.results_text.insert(tk.END, f"📋 {key.upper()}:\n")
                    if isinstance(value, list):
                        for item in value:
                            self.results_text.insert(tk.END, f"  • {item}\n")
                    else:
                        self.results_text.insert(tk.END, f"  {value}\n")
                    self.results_text.insert(tk.END, "\n")
                    
            except Exception as e:
                self.results_text.insert(tk.END, f"❌ Ошибка анализа: {str(e)}\n")
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def smart_scheduling(self):
        """Умное планирование задач"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "🔄 Создаю оптимальное расписание...\n\n")
        self.parent.update()
        
        def schedule():
            try:
                tasks = getattr(self.parent, 'tasks', [])
                if not tasks:
                    self.results_text.insert(tk.END, "❌ Нет задач для планирования.\n")
                    return
                
                schedule = self.ai_assistant.suggest_time_blocks(tasks)
                
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "⏰ Рекомендуемое расписание:\n\n")
                
                for block in schedule:
                    self.results_text.insert(tk.END, f"🕐 {block.get('время_начала', 'N/A')} - {block.get('задача', 'N/A')}\n")
                    self.results_text.insert(tk.END, f"   Продолжительность: {block.get('продолжительность', 'N/A')} мин\n")
                    self.results_text.insert(tk.END, f"   💡 {block.get('обоснование', '')}\n\n")
                    
            except Exception as e:
                self.results_text.insert(tk.END, f"❌ Ошибка планирования: {str(e)}\n")
        
        threading.Thread(target=schedule, daemon=True).start()
    
    def show_productivity_insights(self):
        """Показать инсайты продуктивности"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "🔄 Анализирую вашу продуктивность...\n\n")
        self.parent.update()
        
        def get_insights():
            try:
                # Получаем данные о завершенных задачах
                completed_tasks = [t for t in getattr(self.parent, 'tasks', []) if t.get('status') == 'completed']
                productivity_data = {
                    "total_tasks": len(getattr(self.parent, 'tasks', [])),
                    "completed_tasks": len(completed_tasks),
                    "completion_rate": len(completed_tasks) / max(len(getattr(self.parent, 'tasks', [])), 1) * 100
                }
                
                insights = self.ai_assistant.productivity_insights(completed_tasks, productivity_data)
                
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "📊 Анализ продуктивности:\n\n")
                
                for key, value in insights.items():
                    self.results_text.insert(tk.END, f"📈 {key.upper().replace('_', ' ')}:\n")
                    if isinstance(value, list):
                        for item in value:
                            self.results_text.insert(tk.END, f"  • {item}\n")
                    else:
                        self.results_text.insert(tk.END, f"  {value}\n")
                    self.results_text.insert(tk.END, "\n")
                    
            except Exception as e:
                self.results_text.insert(tk.END, f"❌ Ошибка анализа: {str(e)}\n")
        
        threading.Thread(target=get_insights, daemon=True).start()
    
    def open_chat_window(self):
        """Открыть окно чата с ИИ"""
        if self.chat_window and self.chat_window.winfo_exists():
            self.chat_window.lift()
            return
        
        self.chat_window = tk.Toplevel(self.parent)
        self.chat_window.title("💬 Чат с ИИ-помощником")
        self.chat_window.geometry("600x500")
        
        # Область чата
        chat_frame = tk.Frame(self.chat_window)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.chat_text = tk.Text(chat_frame, height=20, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_text.pack(fill=tk.BOTH, expand=True)
        
        # Поле ввода
        input_frame = tk.Frame(self.chat_window)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.chat_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.chat_entry.bind("<Return>", self.send_message)
        
        send_button = tk.Button(input_frame, text="Отправить", command=self.send_message)
        send_button.pack(side=tk.RIGHT)
        
        # Приветственное сообщение
        self.add_chat_message("🤖 ИИ-Помощник", "Привет! Я ваш персональный помощник по планированию. Задавайте любые вопросы о продуктивности, тайм-менеджменте или планировании задач!")
        
        self.chat_entry.focus()
    
    def send_message(self, event=None):
        """Отправить сообщение в чат"""
        message = self.chat_entry.get().strip()
        if not message:
            return
        
        self.chat_entry.delete(0, tk.END)
        self.add_chat_message("👤 Вы", message)
        
        def get_response():
            try:
                # Подготавливаем контекст
                context = {
                    "total_tasks": len(getattr(self.parent, 'tasks', [])),
                    "current_time": datetime.now().strftime("%H:%M")
                }
                
                response = self.ai_assistant.chat_with_assistant(message, context)
                self.add_chat_message("🤖 ИИ-Помощник", response)
            except Exception as e:
                self.add_chat_message("🤖 ИИ-Помощник", f"Извините, произошла ошибка: {str(e)}")
        
        threading.Thread(target=get_response, daemon=True).start()
    
    def add_chat_message(self, sender: str, message: str):
        """Добавить сообщение в чат"""
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, f"\n{sender}:\n{message}\n")
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)


# Функция для интеграции с основным приложением
def integrate_ai_assistant(main_app, api_key: str):
    """Интегрировать ИИ-помощника в основное приложение"""
    try:
        ai_assistant = AIAssistant(api_key)
        ai_ui = AIAssistantUI(main_app, ai_assistant)
        
        # Добавляем вкладку ИИ-помощника если есть notebook
        if hasattr(main_app, 'notebook'):
            ai_ui.create_ai_tab(main_app.notebook)
        
        # Сохраняем ссылки в основном приложении
        main_app.ai_assistant = ai_assistant
        main_app.ai_ui = ai_ui
        
        return True
    except Exception as e:
        logging.error(f"Failed to integrate AI assistant: {str(e)}")
        return False
