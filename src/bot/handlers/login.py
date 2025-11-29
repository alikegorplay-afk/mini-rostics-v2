from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ...managers.login_manager import UserManager


def get_auth_router(user_manager: UserManager):
    router = Router()
    
    @router.message(Command("login"))
    async def auth(message: Message):
        try:
            _, login, password = message.text.split()
            result, text = await user_manager.auth(login, password, message.chat.id) 
            await message.answer(
                (
                    f"{text}\n"
                    f"Код ответа: {result}"
                )
            )
        except ValueError:
            await message.answer(
                (
                    "Пожалуйста введите в формате:\n"
                    "<code>/login [логин] [пароль]</code>"
                )
            )
            
    return router