from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def add_product(message: Message, state: FSMContext):
    await state.clear()

