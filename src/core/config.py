import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    """Конфигурация приложения"""
    BOT_TOKEN: Optional[str] = None
    API_TOKEN: Optional[str] = None
    
    def __post_init__(self):
        self.BOT_TOKEN = os.getenv("BOT_TOKEN")
        self.API_TOKEN = os.getenv("API_TOKEN")
        self.DEBUG = bool(os.getenv("DEBUG")) if os.getenv("DEBUG") else False
        self._validate()
    
    def _validate(self):
        """Проверка обязательных параметров"""
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN не установлен")
        if not self.API_TOKEN:
            raise ValueError("API_TOKEN не установлен")
    
    @property
    def is_configured(self) -> bool:
        """Проверка, что все обязательные параметры установлены"""
        return all([self.BOT_TOKEN, self.API_TOKEN])


config = Config()