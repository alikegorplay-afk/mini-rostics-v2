from pathlib import Path
from typing import Dict, Any

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from aiogram import Router, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import Command 
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .update import update_init
from ...api.schemas import ProductSchema
from ...core.database.models import OrderStatus

def create_manager(session_maker: async_sessionmaker[AsyncSession]):
    from ...managers import OrderManager
    return OrderManager(session_maker)

def product_manager(session_maker: async_sessionmaker[AsyncSession]):
    from ...managers import ProductManager
    return ProductManager(session_maker)

def init_order_router(session_maker: async_sessionmaker[AsyncSession]):
    api = create_manager(session_maker)
    product_api = product_manager(session_maker)
    router = Router()
    
    @router.callback_query(F.data.startswith("updord-"))
    async def update_order(call: CallbackQuery):
        order_id = int(call.data.split('-')[1])
        await api.update_status(order_id, OrderStatus.PAID)
        await call.message.delete()
        order = await api.get_order(order_id)
        ids = {x.product_id: x.count for x in order.items}
        items = await product_api.get_products([x for x in ids.keys()])
        total_price = sum([x.price * ids[x.id] for x in items])
        await call.message.answer(
(
f"""ID заказа <b>{order.id}</b>
Статус заказа <b>{order.status}</b>
Итоговая цена заказа <b>{total_price} руб.</b>\n
В заказ входят такие продукты как:\n
{'\n'.join(
    [f"{x.id}. {x.title} - {x.price} руб" for x in items]
)}
"""
)
        )
    
    @router.message(Command("getord"))
    async def get_order(message: Message):
        try:
            _, id = message.text.split()
            id = int(id)
            
            order = await api.get_order(id)
            if not order:
                await message.answer(f"Не найден заказ по ID {id}")
                return
            ids = {x.product_id: x.count for x in order.items}
            items = await product_api.get_products([x for x in ids.keys()])
            total_price = sum([x.price * ids[x.id] for x in items])
            await message.answer(
                (
f"""ID заказа <b>{order.id}</b>
Статус заказа <b>{order.status}</b>
Итоговая цена заказа <b>{total_price} руб.</b>\n
В заказ входят такие продукты как:\n
{'\n'.join(
    [f"{x.id}. {x.title} - {x.price} руб" for x in items]
)}
"""
                ), reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="Обновить статус", 
                                              callback_data=f'updord-{order.id}')]
                    ]
                )
            )
        except ValueError:
            await message.answer(
                (
                    "Пожалуйста введите в формате:\n"
                    "<code>/getord [ID заказа]</code>"
                )
            )
            
    return router