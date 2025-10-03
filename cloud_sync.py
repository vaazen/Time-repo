# cloud_sync.py - Облачная синхронизация и экспорт данных
import json
import os
import requests
from datetime import datetime
from typing import Dict, List, Optional
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import dropbox
import pickle
import base64

class CloudSyncManager(QObject):
    """Менеджер облачной синхронизации"""
    
    sync_progress = pyqtSignal(int)  # Прогресс синхронизации
    sync_completed = pyqtSignal(bool, str)  # Успех, сообщение
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dropbox_client = None
        self.google_drive_client = None
        
    def setup_dropbox(self, access_token: str):
        """Настройка Dropbox"""
        try:
            self.dropbox_client = dropbox.Dropbox(access_token)
            return True
        except Exception as e:
            print(f"Ошибка настройки Dropbox: {e}")
            return False
    
    def sync_to_dropbox(self, data: Dict):
        """Синхронизация с Dropbox"""
        if not self.dropbox_client:
            return False
            
        try:
            # Конвертируем данные в JSON
            json_data = json.dumps(data, ensure_ascii=False, indent=2, default=str)
            
            # Загружаем в Dropbox
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/TimeBlocking_backup_{timestamp}.json"
            
            self.dropbox_client.files_upload(
                json_data.encode('utf-8'),
                filename,
                mode=dropbox.files.WriteMode.overwrite
            )
            
            self.sync_completed.emit(True, "Данные успешно синхронизированы с Dropbox")
            return True
            
        except Exception as e:
            self.sync_completed.emit(False, f"Ошибка синхронизации: {e}")
            return False

class DataExporter:
    """Экспортер данных в различные форматы"""
    
    def __init__(self):
        self.supported_formats = ['json', 'csv', 'xlsx', 'pdf']
    
    def export_to_json(self, data: Dict, filename: str) -> bool:
        """Экспорт в JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Ошибка экспорта в JSON: {e}")
            return False
    
    def export_to_csv(self, tasks_data: List[Dict], filename: str) -> bool:
        """Экспорт задач в CSV"""
        try:
            import pandas as pd
            df = pd.DataFrame(tasks_data)
            df.to_csv(filename, index=False, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Ошибка экспорта в CSV: {e}")
            return False
    
    def export_to_excel(self, data: Dict, filename: str) -> bool:
        """Экспорт в Excel с несколькими листами"""
        try:
            import pandas as pd
            
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Лист с задачами
                if 'tasks' in data:
                    tasks_df = pd.DataFrame(data['tasks'])
                    tasks_df.to_excel(writer, sheet_name='Задачи', index=False)
                
                # Лист со статистикой
                if 'statistics' in data:
                    stats_df = pd.DataFrame([data['statistics']])
                    stats_df.to_excel(writer, sheet_name='Статистика', index=False)
                
                # Лист с настройками
                if 'settings' in data:
                    settings_df = pd.DataFrame([data['settings']])
                    settings_df.to_excel(writer, sheet_name='Настройки', index=False)
            
            return True
        except Exception as e:
            print(f"Ошибка экспорта в Excel: {e}")
            return False

# Глобальные экземпляры
cloud_sync_manager = CloudSyncManager()
data_exporter = DataExporter()
