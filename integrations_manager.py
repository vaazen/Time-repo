"""
🔗 Менеджер интеграций с внешними сервисами
Поддерживает Slack, Trello, Notion
"""

import requests
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any
import tkinter as tk
from tkinter import messagebox, simpledialog
import threading

class SlackIntegration:
    """Интеграция со Slack"""
    
    def __init__(self, bot_token: str = None, webhook_url: str = None):
        self.bot_token = bot_token
        self.webhook_url = webhook_url
        self.base_url = "https://slack.com/api"
        self.headers = {"Authorization": f"Bearer {bot_token}"} if bot_token else {}
        
    def send_task_notification(self, task: Dict, channel: str = "#general") -> bool:
        """Отправить уведомление о задаче в Slack"""
        try:
            message = {
                "channel": channel,
                "text": f"📋 Новая задача: {task.get('title', 'Без названия')}",
                "attachments": [
                    {
                        "color": "good",
                        "fields": [
                            {"title": "Описание", "value": task.get('description', 'Нет описания'), "short": False},
                            {"title": "Приоритет", "value": task.get('priority', 'medium'), "short": True},
                            {"title": "Дедлайн", "value": task.get('deadline', 'Не указан'), "short": True}
                        ]
                    }
                ]
            }
            
            if self.webhook_url:
                response = requests.post(self.webhook_url, json=message)
                return response.status_code == 200
            elif self.bot_token:
                response = requests.post(f"{self.base_url}/chat.postMessage", 
                                       headers=self.headers, json=message)
                return response.status_code == 200
            return False
        except Exception as e:
            logging.error(f"Slack notification failed: {e}")
            return False
    
    def get_channels(self) -> List[Dict]:
        """Получить список каналов"""
        try:
            if not self.bot_token:
                return []
            
            response = requests.get(f"{self.base_url}/conversations.list", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                return data.get('channels', [])
            return []
        except Exception as e:
            logging.error(f"Failed to get Slack channels: {e}")
            return []

class TrelloIntegration:
    """Интеграция с Trello"""
    
    def __init__(self, api_key: str = None, token: str = None):
        self.api_key = api_key
        self.token = token
        self.base_url = "https://api.trello.com/1"
        
    def create_card(self, board_id: str, list_id: str, task: Dict) -> Optional[str]:
        """Создать карточку в Trello"""
        try:
            url = f"{self.base_url}/cards"
            params = {
                "key": self.api_key,
                "token": self.token,
                "idList": list_id,
                "name": task.get('title', 'Новая задача'),
                "desc": task.get('description', ''),
                "due": task.get('deadline', None)
            }
            
            response = requests.post(url, params=params)
            if response.status_code == 200:
                card_data = response.json()
                return card_data.get('id')
            return None
        except Exception as e:
            logging.error(f"Trello card creation failed: {e}")
            return None
    
    def get_boards(self) -> List[Dict]:
        """Получить список досок"""
        try:
            url = f"{self.base_url}/members/me/boards"
            params = {"key": self.api_key, "token": self.token}
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            logging.error(f"Failed to get Trello boards: {e}")
            return []
    
    def get_lists(self, board_id: str) -> List[Dict]:
        """Получить списки доски"""
        try:
            url = f"{self.base_url}/boards/{board_id}/lists"
            params = {"key": self.api_key, "token": self.token}
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            logging.error(f"Failed to get Trello lists: {e}")
            return []

class NotionIntegration:
    """Интеграция с Notion"""
    
    def __init__(self, token: str = None):
        self.token = token
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        } if token else {}
    
    def create_page(self, database_id: str, task: Dict) -> Optional[str]:
        """Создать страницу в базе данных Notion"""
        try:
            url = f"{self.base_url}/pages"
            
            properties = {
                "Название": {"title": [{"text": {"content": task.get('title', 'Новая задача')}}]},
                "Статус": {"select": {"name": task.get('status', 'Не начато')}},
                "Приоритет": {"select": {"name": task.get('priority', 'Средний')}}
            }
            
            if task.get('deadline'):
                properties["Дедлайн"] = {"date": {"start": task['deadline']}}
            
            data = {
                "parent": {"database_id": database_id},
                "properties": properties
            }
            
            if task.get('description'):
                data["children"] = [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": task['description']}}]
                        }
                    }
                ]
            
            response = requests.post(url, headers=self.headers, json=data)
            if response.status_code == 200:
                page_data = response.json()
                return page_data.get('id')
            return None
        except Exception as e:
            logging.error(f"Notion page creation failed: {e}")
            return None
    
    def get_databases(self) -> List[Dict]:
        """Получить список баз данных"""
        try:
            url = f"{self.base_url}/search"
            data = {"filter": {"value": "database", "property": "object"}}
            
            response = requests.post(url, headers=self.headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result.get('results', [])
            return []
        except Exception as e:
            logging.error(f"Failed to get Notion databases: {e}")
            return []

class IntegrationsManager:
    """Менеджер всех интеграций"""
    
    def __init__(self):
        self.slack = None
        self.trello = None
        self.notion = None
        self.settings = {}
        
    def setup_slack(self, bot_token: str = None, webhook_url: str = None):
        """Настроить интеграцию со Slack"""
        self.slack = SlackIntegration(bot_token, webhook_url)
        self.settings['slack'] = {'bot_token': bot_token, 'webhook_url': webhook_url}
        
    def setup_trello(self, api_key: str, token: str):
        """Настроить интеграцию с Trello"""
        self.trello = TrelloIntegration(api_key, token)
        self.settings['trello'] = {'api_key': api_key, 'token': token}
        
    def setup_notion(self, token: str):
        """Настроить интеграцию с Notion"""
        self.notion = NotionIntegration(token)
        self.settings['notion'] = {'token': token}
    
    def sync_task_to_all(self, task: Dict) -> Dict[str, bool]:
        """Синхронизировать задачу со всеми сервисами"""
        results = {}
        
        # Slack
        if self.slack:
            results['slack'] = self.slack.send_task_notification(task)
        
        # Trello
        if self.trello and self.settings.get('trello', {}).get('default_board'):
            board_id = self.settings['trello']['default_board']
            list_id = self.settings['trello'].get('default_list')
            if list_id:
                card_id = self.trello.create_card(board_id, list_id, task)
                results['trello'] = card_id is not None
        
        # Notion
        if self.notion and self.settings.get('notion', {}).get('default_database'):
            database_id = self.settings['notion']['default_database']
            page_id = self.notion.create_page(database_id, task)
            results['notion'] = page_id is not None
        
        return results

class IntegrationsUI:
    """Интерфейс для управления интеграциями"""
    
    def __init__(self, parent, integrations_manager: IntegrationsManager):
        self.parent = parent
        self.manager = integrations_manager
        
    def create_integrations_tab(self, notebook):
        """Создать вкладку интеграций"""
        integrations_frame = tk.Frame(notebook)
        notebook.add(integrations_frame, text="🔗 Интеграции")
        
        # Заголовок
        title_label = tk.Label(integrations_frame, text="🔗 Интеграции с внешними сервисами", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Slack секция
        slack_frame = tk.LabelFrame(integrations_frame, text="📱 Slack", font=("Arial", 12, "bold"))
        slack_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(slack_frame, text="Настроить Slack", command=self.setup_slack_dialog).pack(pady=5)
        tk.Button(slack_frame, text="Тест уведомления", command=self.test_slack).pack(pady=5)
        
        # Trello секция
        trello_frame = tk.LabelFrame(integrations_frame, text="📋 Trello", font=("Arial", 12, "bold"))
        trello_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(trello_frame, text="Настроить Trello", command=self.setup_trello_dialog).pack(pady=5)
        tk.Button(trello_frame, text="Выбрать доску", command=self.select_trello_board).pack(pady=5)
        
        # Notion секция
        notion_frame = tk.LabelFrame(integrations_frame, text="📝 Notion", font=("Arial", 12, "bold"))
        notion_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(notion_frame, text="Настроить Notion", command=self.setup_notion_dialog).pack(pady=5)
        tk.Button(notion_frame, text="Выбрать базу данных", command=self.select_notion_database).pack(pady=5)
        
        # Статус интеграций
        self.status_text = tk.Text(integrations_frame, height=10, width=60)
        self.status_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.update_status()
        
        return integrations_frame
    
    def setup_slack_dialog(self):
        """Диалог настройки Slack"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Настройка Slack")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="Выберите способ интеграции:", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Webhook URL
        tk.Label(dialog, text="Webhook URL (рекомендуется):").pack(anchor=tk.W, padx=10)
        webhook_entry = tk.Entry(dialog, width=50)
        webhook_entry.pack(padx=10, pady=5)
        
        tk.Label(dialog, text="ИЛИ Bot Token:").pack(anchor=tk.W, padx=10, pady=(20, 0))
        token_entry = tk.Entry(dialog, width=50, show="*")
        token_entry.pack(padx=10, pady=5)
        
        def save_slack():
            webhook = webhook_entry.get().strip()
            token = token_entry.get().strip()
            
            if webhook or token:
                self.manager.setup_slack(token if token else None, webhook if webhook else None)
                messagebox.showinfo("Успех", "Slack интеграция настроена!")
                self.update_status()
                dialog.destroy()
            else:
                messagebox.showerror("Ошибка", "Введите Webhook URL или Bot Token")
        
        tk.Button(dialog, text="Сохранить", command=save_slack, bg="#4CAF50", fg="white").pack(pady=20)
    
    def setup_trello_dialog(self):
        """Диалог настройки Trello"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Настройка Trello")
        dialog.geometry("400x250")
        
        tk.Label(dialog, text="API Key:", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 0))
        api_key_entry = tk.Entry(dialog, width=50)
        api_key_entry.pack(padx=10, pady=5)
        
        tk.Label(dialog, text="Token:", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=10)
        token_entry = tk.Entry(dialog, width=50, show="*")
        token_entry.pack(padx=10, pady=5)
        
        def save_trello():
            api_key = api_key_entry.get().strip()
            token = token_entry.get().strip()
            
            if api_key and token:
                self.manager.setup_trello(api_key, token)
                messagebox.showinfo("Успех", "Trello интеграция настроена!")
                self.update_status()
                dialog.destroy()
            else:
                messagebox.showerror("Ошибка", "Введите API Key и Token")
        
        tk.Button(dialog, text="Сохранить", command=save_trello, bg="#0079BF", fg="white").pack(pady=20)
    
    def setup_notion_dialog(self):
        """Диалог настройки Notion"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Настройка Notion")
        dialog.geometry("400x200")
        
        tk.Label(dialog, text="Integration Token:", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 0))
        token_entry = tk.Entry(dialog, width=50, show="*")
        token_entry.pack(padx=10, pady=5)
        
        def save_notion():
            token = token_entry.get().strip()
            
            if token:
                self.manager.setup_notion(token)
                messagebox.showinfo("Успех", "Notion интеграция настроена!")
                self.update_status()
                dialog.destroy()
            else:
                messagebox.showerror("Ошибка", "Введите Integration Token")
        
        tk.Button(dialog, text="Сохранить", command=save_notion, bg="#000000", fg="white").pack(pady=20)
    
    def test_slack(self):
        """Тест уведомления Slack"""
        if not self.manager.slack:
            messagebox.showerror("Ошибка", "Сначала настройте Slack интеграцию")
            return
        
        test_task = {
            "title": "Тестовая задача",
            "description": "Это тестовое уведомление из Time Blocking App",
            "priority": "high",
            "deadline": datetime.now().strftime("%Y-%m-%d")
        }
        
        success = self.manager.slack.send_task_notification(test_task)
        if success:
            messagebox.showinfo("Успех", "Тестовое уведомление отправлено!")
        else:
            messagebox.showerror("Ошибка", "Не удалось отправить уведомление")
    
    def select_trello_board(self):
        """Выбор доски Trello"""
        if not self.manager.trello:
            messagebox.showerror("Ошибка", "Сначала настройте Trello интеграцию")
            return
        
        def load_boards():
            boards = self.manager.trello.get_boards()
            if boards:
                board_names = [f"{board['name']} ({board['id']})" for board in boards]
                selected = simpledialog.askstring("Выбор доски", f"Доступные доски:\n" + "\n".join(board_names) + "\n\nВведите ID доски:")
                if selected:
                    self.manager.settings.setdefault('trello', {})['default_board'] = selected
                    messagebox.showinfo("Успех", f"Выбрана доска: {selected}")
            else:
                messagebox.showerror("Ошибка", "Не удалось загрузить доски")
        
        threading.Thread(target=load_boards, daemon=True).start()
    
    def select_notion_database(self):
        """Выбор базы данных Notion"""
        if not self.manager.notion:
            messagebox.showerror("Ошибка", "Сначала настройте Notion интеграцию")
            return
        
        def load_databases():
            databases = self.manager.notion.get_databases()
            if databases:
                db_names = [f"{db.get('title', [{}])[0].get('plain_text', 'Без названия')} ({db['id']})" for db in databases]
                selected = simpledialog.askstring("Выбор базы данных", f"Доступные базы данных:\n" + "\n".join(db_names) + "\n\nВведите ID базы данных:")
                if selected:
                    self.manager.settings.setdefault('notion', {})['default_database'] = selected
                    messagebox.showinfo("Успех", f"Выбрана база данных: {selected}")
            else:
                messagebox.showerror("Ошибка", "Не удалось загрузить базы данных")
        
        threading.Thread(target=load_databases, daemon=True).start()
    
    def update_status(self):
        """Обновить статус интеграций"""
        self.status_text.delete(1.0, tk.END)
        
        status_text = "📊 Статус интеграций:\n\n"
        
        # Slack
        if self.manager.slack:
            status_text += "✅ Slack: Настроен\n"
        else:
            status_text += "❌ Slack: Не настроен\n"
        
        # Trello
        if self.manager.trello:
            status_text += "✅ Trello: Настроен\n"
        else:
            status_text += "❌ Trello: Не настроен\n"
        
        # Notion
        if self.manager.notion:
            status_text += "✅ Notion: Настроен\n"
        else:
            status_text += "❌ Notion: Не настроен\n"
        
        status_text += "\n📋 Настройки:\n"
        for service, settings in self.manager.settings.items():
            status_text += f"  {service.upper()}:\n"
            for key, value in settings.items():
                if 'token' in key.lower() or 'key' in key.lower():
                    value = "***скрыто***" if value else "не задано"
                status_text += f"    {key}: {value}\n"
        
        self.status_text.insert(1.0, status_text)

def integrate_external_services(main_app):
    """Интегрировать внешние сервисы в основное приложение"""
    try:
        integrations_manager = IntegrationsManager()
        integrations_ui = IntegrationsUI(main_app, integrations_manager)
        
        # Добавляем вкладку интеграций
        if hasattr(main_app, 'notebook'):
            integrations_ui.create_integrations_tab(main_app.notebook)
        
        # Сохраняем ссылки в основном приложении
        main_app.integrations_manager = integrations_manager
        main_app.integrations_ui = integrations_ui
        
        return True
    except Exception as e:
        logging.error(f"Failed to integrate external services: {str(e)}")
        return False
