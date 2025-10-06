"""
🔧 Централизованная система управления конфигурацией
Обеспечивает гибкую настройку приложения через файлы конфигурации и переменные окружения
"""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

@dataclass
class UIConfig:
    """Конфигурация пользовательского интерфейса"""
    language: str = "ru"
    theme: str = "dark"
    animations_enabled: bool = True
    window_width: int = 1200
    window_height: int = 800
    auto_save_interval: int = 30  # секунды
    font_size: int = 12
    show_notifications: bool = True

@dataclass
class AIConfig:
    """Конфигурация ИИ-помощника"""
    provider: str = "openai"
    api_key: str = ""
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 1000
    temperature: float = 0.7
    offline_mode: bool = False
    max_retries: int = 3

@dataclass
class IntegrationsConfig:
    """Конфигурация интеграций"""
    slack_enabled: bool = False
    slack_webhook_url: str = ""
    slack_bot_token: str = ""
    trello_enabled: bool = False
    trello_api_key: str = ""
    trello_token: str = ""
    notion_enabled: bool = False
    notion_token: str = ""
    dropbox_enabled: bool = False
    dropbox_token: str = ""

@dataclass
class DataConfig:
    """Конфигурация данных"""
    backup_enabled: bool = True
    backup_interval_hours: int = 24
    cloud_sync: bool = False
    export_format: str = "json"
    data_retention_days: int = 365
    cache_enabled: bool = True
    cache_size_mb: int = 100

@dataclass
class PerformanceConfig:
    """Конфигурация производительности"""
    async_operations: bool = True
    max_concurrent_tasks: int = 10
    ui_update_interval_ms: int = 1000
    analytics_update_interval_ms: int = 5000
    lazy_loading: bool = True
    memory_limit_mb: int = 512

@dataclass
class AppConfig:
    """Основная конфигурация приложения"""
    ui: UIConfig
    ai: AIConfig
    integrations: IntegrationsConfig
    data: DataConfig
    performance: PerformanceConfig
    debug_mode: bool = False
    log_level: str = "INFO"

class ConfigManager:
    """Менеджер конфигурации приложения"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config.json"
        self.config_dir = Path(self.config_path).parent
        self.config_dir.mkdir(exist_ok=True)
        
        self.logger = logging.getLogger(__name__)
        self._config: Optional[AppConfig] = None
        
        # Создаем конфигурацию по умолчанию
        self._default_config = AppConfig(
            ui=UIConfig(),
            ai=AIConfig(),
            integrations=IntegrationsConfig(),
            data=DataConfig(),
            performance=PerformanceConfig()
        )
    
    def load_config(self) -> AppConfig:
        """Загрузка конфигурации из файла и переменных окружения"""
        try:
            # Загружаем из файла
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                self._config = self._dict_to_config(config_data)
            else:
                self._config = self._default_config
                self.save_config()  # Создаем файл конфигурации по умолчанию
            
            # Переопределяем значениями из переменных окружения
            self._apply_env_variables()
            
            self.logger.info(f"Конфигурация загружена из {self.config_path}")
            return self._config
            
        except Exception as e:
            self.logger.error(f"Ошибка загрузки конфигурации: {e}")
            self._config = self._default_config
            return self._config
    
    def save_config(self) -> bool:
        """Сохранение конфигурации в файл"""
        try:
            if self._config is None:
                self._config = self._default_config
            
            config_dict = self._config_to_dict(self._config)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Конфигурация сохранена в {self.config_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка сохранения конфигурации: {e}")
            return False
    
    def get_config(self) -> AppConfig:
        """Получение текущей конфигурации"""
        if self._config is None:
            return self.load_config()
        return self._config
    
    def update_config(self, **kwargs) -> bool:
        """Обновление конфигурации"""
        try:
            if self._config is None:
                self._config = self.load_config()
            
            # Обновляем значения
            for key, value in kwargs.items():
                if hasattr(self._config, key):
                    setattr(self._config, key, value)
            
            return self.save_config()
            
        except Exception as e:
            self.logger.error(f"Ошибка обновления конфигурации: {e}")
            return False
    
    def _dict_to_config(self, config_dict: Dict[str, Any]) -> AppConfig:
        """Преобразование словаря в объект конфигурации"""
        return AppConfig(
            ui=UIConfig(**config_dict.get('ui', {})),
            ai=AIConfig(**config_dict.get('ai', {})),
            integrations=IntegrationsConfig(**config_dict.get('integrations', {})),
            data=DataConfig(**config_dict.get('data', {})),
            performance=PerformanceConfig(**config_dict.get('performance', {})),
            debug_mode=config_dict.get('debug_mode', False),
            log_level=config_dict.get('log_level', 'INFO')
        )
    
    def _config_to_dict(self, config: AppConfig) -> Dict[str, Any]:
        """Преобразование объекта конфигурации в словарь"""
        return {
            'ui': asdict(config.ui),
            'ai': asdict(config.ai),
            'integrations': asdict(config.integrations),
            'data': asdict(config.data),
            'performance': asdict(config.performance),
            'debug_mode': config.debug_mode,
            'log_level': config.log_level
        }
    
    def _apply_env_variables(self):
        """Применение переменных окружения"""
        if self._config is None:
            return
        
        # ИИ настройки
        if api_key := os.getenv('OPENAI_API_KEY'):
            self._config.ai.api_key = api_key
        if model := os.getenv('AI_MODEL'):
            self._config.ai.model = model
        
        # Интеграции
        if slack_webhook := os.getenv('SLACK_WEBHOOK_URL'):
            self._config.integrations.slack_webhook_url = slack_webhook
            self._config.integrations.slack_enabled = True
        
        if trello_key := os.getenv('TRELLO_API_KEY'):
            self._config.integrations.trello_api_key = trello_key
        if trello_token := os.getenv('TRELLO_TOKEN'):
            self._config.integrations.trello_token = trello_token
            self._config.integrations.trello_enabled = True
        
        if notion_token := os.getenv('NOTION_TOKEN'):
            self._config.integrations.notion_token = notion_token
            self._config.integrations.notion_enabled = True
        
        if dropbox_token := os.getenv('DROPBOX_ACCESS_TOKEN'):
            self._config.integrations.dropbox_token = dropbox_token
            self._config.integrations.dropbox_enabled = True
        
        # Отладка
        if debug := os.getenv('DEBUG'):
            self._config.debug_mode = debug.lower() in ('true', '1', 'yes')
        
        if log_level := os.getenv('LOG_LEVEL'):
            self._config.log_level = log_level.upper()

# Глобальный экземпляр менеджера конфигурации
config_manager = ConfigManager()

def get_config() -> AppConfig:
    """Получение глобальной конфигурации"""
    return config_manager.get_config()

def save_config() -> bool:
    """Сохранение глобальной конфигурации"""
    return config_manager.save_config()

def update_config(**kwargs) -> bool:
    """Обновление глобальной конфигурации"""
    return config_manager.update_config(**kwargs)

# Инициализация при импорте
_config = config_manager.load_config()
