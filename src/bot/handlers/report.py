import aiofiles

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from aiogram import Router
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command
from loguru import logger

from ...service.orders import OrderProductService
from ...core.const import REPORT_PATH


def get_report_router(session_maker: async_sessionmaker[AsyncSession]):
    router = Router()
    
    api = OrderProductService(session_maker)
    @router.message(Command("report"))
    async def get_report(message: Message):
        try:
            await message.bot.send_chat_action(message.chat.id, 'upload_document')
            report = await api.generate_report()
            if report:
                async with aiofiles.open(REPORT_PATH, 'rb') as f:
                    await message.answer_document(BufferedInputFile(await f.read(), str(REPORT_PATH)), caption="Ваш отчет!")
            else:
                await message.answer("Не удлаось сгенерировать отчёт пожалуйтса сделайте это позже!")
        except Exception as e:
            logger.error(f"Ошибка при попытке отправить отчёт: {e}")
            await message.answer("Ой! У нас неполадки пожалуйста сделайте запрос позже")
    
    return router