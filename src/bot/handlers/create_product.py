from pathlib import Path
from typing import Dict, Any

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command 
from aiogram.fsm.context import FSMContext

from ..state import AddProduct
from ...core.const import PATH_TO_SAVE_IMAGE
from ...schemas import ProductCreateSchema
from ...tools import get_poster
from ...managers.login_manager import UserManager

def create_manager(session_maker: async_sessionmaker[AsyncSession]):
    from ...managers import ProductManager
    return ProductManager(session_maker)


def product_add_router(session_maker: async_sessionmaker[AsyncSession], user_manager: UserManager):
    router = Router()
    manager = create_manager(session_maker)

    @router.message(Command("addprod"))
    async def add_product(message: Message, state: FSMContext):
        if not await user_manager.is_auth(message.chat.id):
            await message.answer(
                "У вас нет прав на это действие"
            )
            return
        await message.answer("Введите название товара:")
        await state.set_state(AddProduct.waiting_for_title)
        
    @router.message(AddProduct.waiting_for_title, F.text)
    async def get_title(message: Message, state: FSMContext):
        await state.update_data(title = message.text)
        await message.answer("Введите описание товара:")
        await state.set_state(AddProduct.waiting_for_description)
        
    @router.message(AddProduct.waiting_for_description, F.text)
    async def get_description(message: Message, state: FSMContext):
        await state.update_data(description = message.text)
        await message.answer("Теперь введите цену товара (только числа):")
        await state.set_state(AddProduct.waiting_for_price)
    
    @router.message(AddProduct.waiting_for_price, F.text)
    async def get_price(message: Message, state: FSMContext):
        try:
            price = float(message.text)
            if price > 1_000_000 or price < 1:
                await message.answer("Слишком высокая/малая цена! Пишите цены в диапазоне от 1 до 1 000 000")
                return
            await state.update_data(price = price)
            await message.answer("Введите количество товара:")
            await state.set_state(AddProduct.waiting_for_count)
        except ValueError:
            await message.answer("Пожалуйста, введите корректную цену (число):")
            
    @router.message(AddProduct.waiting_for_count, F.text)
    async def get_count(message: Message, state: FSMContext):
        try:
            count = float(message.text)
            if not count.is_integer():
                await message.answer("Пожалуйста введите целое число")
                return
            if count > 100_000 or count < 1:
                await message.answer("Слишком много/мало товаров! Пишите в диапазоне от 1 до 100 000")
                return
            await message.answer("Пришлите постер:")
            await state.update_data(count = count)
            await state.set_state(AddProduct.waiting_for_poster)
        except ValueError:
            await message.answer("Пожалуйста, введите корректное количество (число):")
            
    @router.message(AddProduct.waiting_for_poster, F.photo)
    async def get_photo(message: Message, state: FSMContext):
        photo = message.photo[-1]
        photo_id = photo.file_id
        
        data = await state.get_data()
        file = await message.bot.get_file(photo_id)
        PATH_TO_SAVE_IMAGE.mkdir(parents=True, exist_ok=True)
        download_path = PATH_TO_SAVE_IMAGE / (photo_id + Path(file.file_path).suffix if file.file_path else ".jpg")
        
        await message.bot.download_file(file.file_path, download_path)
        try:
            product = await add_data(data, download_path)
        except Exception as e:
            await message.answer(f"Ошибка при добавлении продукта: {str(e)}")
            return
        
        await message.answer_photo(
            get_poster(product.poster),
            caption = (
                f"Продукт под ID <b>{product.id}</b> успешно добавлен\n"
                f"Название продукции <b>{product.title}</b>\n"
                f"Цена за еденицу продукции <b>{product.price}</b>\n"
                f"Количество продукции на складе <b>{product.count}</b>\n\n"
                f"DEBUG:\n"
                f"Путь к постеру: {product.poster}"
            )
        )
        await state.clear()
        
    async def add_data(data: Dict[str, Any], download_path: Path):
        return await manager.create_product(
            ProductCreateSchema(
                **data,
                poster = str(download_path).replace("\\", "/")
            )
        )
    
    return router