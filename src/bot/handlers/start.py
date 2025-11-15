from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ..answers import HELLO_TXT, HELP_TXT

router = Router()

@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer(
        HELLO_TXT,
        parse_mode="HTML"
    )
    await state.clear()
    
@router.message(Command("help"))
async def help(message: Message):
    await message.answer(
        HELP_TXT,
        parse_mode="HTML"
    )
    
@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    await message.answer("Сброс всех позиций")
    await state.clear()