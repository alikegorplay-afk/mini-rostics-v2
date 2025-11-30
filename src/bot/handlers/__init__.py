from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from .start import router as start_router
from .product import product_api_router
from .create_product import product_add_router
from .order import init_order_router
from .login import get_auth_router
from .report import get_report_router
from ...managers.login_manager import UserManager

router = Router()

@router.message(F.text.startswith('/'))
async def unknown_command(message: Message):
    await message.answer("Я вас не понял. Пропишите /help для того чтобы ознакомиться с командами")


def init(session_maker: async_sessionmaker[AsyncSession]):
    user_manager = UserManager()

    product_router = product_add_router(session_maker, user_manager)
    product_api = product_api_router(session_maker, user_manager)
    order = init_order_router(session_maker, user_manager)
    login_api = get_auth_router(user_manager)
    report_api = get_report_router(session_maker)
    
    return [start_router, product_api, product_router, order, login_api, report_api, router]