import asyncio
import logging

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger

async def set_command(bot: Bot):
    command = [
        BotCommand(command="start", description="Начать всё сначала"),
        BotCommand(command="cancel", description="Сброс всех состояний"),
        BotCommand(command="addprod", description="Добавить продукты"),
    ]
    await bot.set_my_commands(command)

from ..core.config import config
from .handlers import init

async def main(session_maker: async_sessionmaker[AsyncSession]):
    logger.info("Запуск бота...")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    logger.info("Инициализация команд...")
    await set_command(bot)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    dp.include_routers(*init(session_maker))
    logger.info("Команды инициализированы")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Бот запущен и начал обработку сообщений")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()