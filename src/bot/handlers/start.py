from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ..answers import HELLO_TXT, HELP_TXT

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        HELLO_TXT,
        parse_mode="HTML"
    )
    
@router.message(Command("help"))
async def help(message: Message):
    await message.answer(
        HELP_TXT,
        parse_mode="HTML"
    )