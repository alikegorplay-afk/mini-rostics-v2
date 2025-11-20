
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command 
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .update import update_init
from ...schemas import ProductSchema

def create_manager(session_maker: async_sessionmaker[AsyncSession]):
    from ...managers import ProductManager
    return ProductManager(session_maker)

def select_keyborad(product: ProductSchema):
    return InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(text="Обновить название", callback_data=f"updtitle-{product.id}")],
            [InlineKeyboardButton(text="Обновить цену", callback_data=f"updprice-{product.id}")],
            [InlineKeyboardButton(text="Обновить Количество товаров", callback_data=f"updcount-{product.id}")],
            [InlineKeyboardButton(text="Обновить описание", callback_data=f"updesc-{product.id}")],
            [InlineKeyboardButton(text="Обновить постер", callback_data=f"updposter-{product.id}")]
        ]
    )


def product_api_router(session_maker: async_sessionmaker[AsyncSession]):
    router = Router()
    manager = create_manager(session_maker)
    
    @router.message(Command("getprod"))
    async def get_product(message: Message):
        try:
            _, id = message.text.split()
            if not id.isdigit():
                await message.answer("ID должен быть числом")
                return
            product = await manager.get_product(int(id))
            if not product:
                await message.answer(f"Продукт с ID {id} не найден")
                return
            await message.answer_photo(
                FSInputFile(product.poster),
                caption = (
                    f"Продукт под ID: '<b>{product.id}</b>'\n"
                    f"Название продукции: '<b>{product.title}</b>'\n"
                    f"Цена за еденицу продукции: '<b>{product.price}</b>'\n"
                    f"Количество продукции на складе: '<b>{product.count}</b>'\n"
                    f"Описание: '<b>{product.description}</b>'\n\n"
                    f"DEBUG\n"
                    f"Путь к постеру: {product.poster}"
                )
            )
        except ValueError:
            await message.answer(
                (
                    "Пожалуйста введите в формате:\n"
                    "<code>/getprod [ID продукта]</code>"
                )
            )
    
    @router.message(Command("delprod"))
    async def delete_prod(message: Message):
        try:
            _, id = message.text.split()
            if not id.isdigit():
                await message.answer("ID должен быть числом")
                return
            ok, text = await manager.delete_product(int(id))
            await message.answer(
                (
                    "Продукт удалён: " + ("✅" if ok else "❌") + "\n"
                    "Подробнее: " + text
                )
            )
        except ValueError:
            await message.answer(
                (
                    "Пожалуйста введите в формате:\n"
                    "<code>/delprod [ID продукта]</code>"
                )
            )
    
    @router.message(Command("setprod"))
    async def set_prod(message: Message):
        try:
            _, id = message.text.split()
            if not id.isdigit():
                await message.answer("ID должен быть числом")
                return
            product = await manager.get_product(id)
            if not product:
                await message.answer(f"Продукт с ID {id} не найден")
                return
            await message.answer_photo(
                FSInputFile(product.poster),
                caption = (
                    f"Продукт под ID: '<b>{product.id}</b>' успешно обновлён\n"
                    f"Название продукции: '<b>{product.title}</b>'\n"
                    f"Цена за еденицу продукции: '<b>{product.price}</b>'\n"
                    f"Количество продукции на складе: '<b>{product.count}</b>'\n\n"
                    f"DEBUG\n"
                    f"Путь к постеру: {product.poster}"
                ),
                reply_markup=select_keyborad(product)
            )
        except ValueError:
            await message.answer(
                (
                    "Пожалуйста введите в формате:\n"
                    "<code>/setprod [ID продукта]</code>"
                )
            )
            
    router.include_router(update_init(manager)) 
    return router