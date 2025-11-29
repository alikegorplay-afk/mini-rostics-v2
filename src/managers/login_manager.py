import asyncio
from typing import Tuple

from ..core.supersu import SUPER_USER, AUTH_USERS

class UserManager:
    def __init__(self):
        self.lock = asyncio.Lock()
    
    async def auth(self, login: str, password: str, chat_id: int) -> Tuple[int, str]:
        async with self.lock:
            if chat_id in AUTH_USERS:
                return (0, "Вы уже авторизированы!")
            
            if login not in SUPER_USER:
                return (1, "Не существующий пользователь")
            
            elif SUPER_USER[login] != password:
                return (2, "Не правильный пароль")
            
            AUTH_USERS.add(chat_id)
            return (0, "Успешная авторизация!")
    
    async def is_auth(self, chat_id: int):
        return chat_id in AUTH_USERS