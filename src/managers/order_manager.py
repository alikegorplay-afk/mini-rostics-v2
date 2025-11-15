__all__ = [
    "OrderManager"
]

from typing import Literal, Optional, Tuple, List

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from loguru import logger

from ..core import Order, OrderItem
from ..core.database.models import OrderStatus
from ..core.exceptions import OrderNotFoundError
from ..api.schemas import CreateOrderSchema, OrderItemSchema, OrderSchema, OrderItemResponseSchema

class OrderManager:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.Session = session_maker
        logger.debug("Инициализирован Order")
        
    async def create_order(self, order: CreateOrderSchema) -> OrderSchema:
        """Создать заказ"""
        logger.debug(f"🆕 Количество продуктов заказа: {len(order.items)}")
        try:
            async with self.Session() as session:
                async with session.begin():
                    sql_order = Order()
                    for item in order.items:
                        sql_order.append(
                            OrderItem(**item.model_dump())
                        )
                    session.add(sql_order)
                    await session.flush()
                    
                    logger.success(
                        f"✅ Заказ создан: '{sql_order.id}' "
                        f"(ID: {sql_order.id}, Кол-во продуктов: {len(sql_order.items)})"
                    )
                    return OrderSchema(
                        id = sql_order.id,
                        status= sql_order.status,
                        items = [OrderItemResponseSchema(
                            id = x.id,
                            product_id=x.product_id,
                            count=x.count
                        ) for x in sql_order.items]
                    )
                    
        except Exception as e:
            logger.error(
                f"❌ Ошибка создания заказа: {str(e)}"
            )
            raise
        
    async def get_order(self, id: int) -> Optional[OrderSchema]:
        logger.info(f"🔍 Поиск заказа ID: {id}")
        try:
            async with self.Session() as session:
                stmt = select(Order).options(selectinload(Order.items)).where(Order.id == id)
                result = await session.execute(stmt)
                order = result.scalar_one_or_none()
                
                if order:
                    logger.info(
                        f"✅ Найден заказ: '{id}' "
                        f"(ID: {order.id}, Кол-во продуктов: {len(order.items)})"
                    )
                else:
                    logger.warning(f"⚠️ заказ ID: {id} не найден")
                    
                return OrderSchema(
                    id = order.id,
                    status= order.status,
                    items = [OrderItemResponseSchema(
                        id = x.id,
                        product_id=x.product_id,
                        count=x.count
                    ) for x in order.items]
                ) if order else None
                
        except Exception as e:
            logger.error(f"❌ Ошибка поиска заказа ID: {id}: {str(e)}")
            raise
        
    async def delete_order(self, id: int) -> Tuple[bool, str]:
        """Удаление заказа"""
        logger.info(f"🗑️ Удаление заказа ID: {id}")
        
        try:
            async with self.Session() as session:
                async with session.begin():
                    stmt = select(Order).options(selectinload(Order.items)).where(Order.id == id)
                    result = await session.execute(stmt)
                    order = result.scalar_one_or_none()
                    if not order:
                        logger.warning(f"⚠️ заказ ID: {id} не найден для удаления")
                        return False, f"заказ ID: {id} не найден для удаления"
                    
                    await session.delete(order)
                    for items in order:
                        await session.delete(items)
                    
                    logger.success(f"✅ Удален заказ: (ID: {id})")
                    return True, f"Удален заказ: (ID: {id})"
                
        except Exception as e:
            logger.error(f"❌ Ошибка удаления заказа ID: {id}: {str(e)}")
            raise
        
    async def update_order(self, id: int, item_data: OrderItemSchema) -> OrderSchema:
        """Добавить продукт в заказ"""
        logger.info(f"🛒 Добавление продукта в заказ ID: {id}")
        logger.debug(f"Данные позиции: {item_data.model_dump()}")
        
        try:
            async with self.Session() as session:
                async with session.begin():
                    stmt = select(Order).options(selectinload(Order.items)).where(Order.id == id)
                    result = await session.execute(stmt)
                    order = result.scalar_one_or_none()
                    if order is None:
                        logger.error(f"❌ Заказ ID: {id} не найден")
                        raise OrderNotFoundError(f"Заказ {id} не найден")
                    
                    existing_items = {item.product_id: item for item in order}
                    new_item = OrderItem(**item_data.model_dump())
                    new_item.order_id = id
                    
                    if new_item.product_id in existing_items:
                        existing_item = existing_items[new_item.product_id]
                        old_count = existing_item.count
                        existing_item.count = new_item.count
                        logger.info(
                            f"📦 Обновлено количество продукта {new_item.product_id} "
                            f"в заказе {id}: {old_count} → {new_item.count}"
                        )
                
                    else:
                        order.items.append(new_item)
                        logger.info(
                            f"📥 Добавлен новый продукт {new_item.product_id} "
                            f"в заказ {id} (кол-во: {new_item.count})"
                        )
                    await session.flush()
                    logger.success(f"✅ Заказ ID: {id} успешно обновлен")
                    return OrderSchema(
                        id = order.id,
                        status= order.status,
                        items = [OrderItemResponseSchema(
                            id = x.id,
                            product_id=x.product_id,
                            count=x.count
                        ) for x in order.items]
                    )
                    
        except OrderNotFoundError:
            raise
        
        except Exception as e:
            logger.error(f"❌ Ошибка добавления продукта в заказ {id}: {str(e)}")
            raise
        
    async def update_status(self, id: int, status: Literal[OrderStatus.PAID, OrderStatus.UNPAID] = OrderStatus.PAID) -> None:
        """Обновление статуса"""
        logger.info(f"🔄 Обновление статуса об заказе ID: {id}")
        if not hasattr(status, 'value'):
            raise AttributeError("Переданный тип не является Enum")
        
        try:
            async with self.Session() as session:
                async with session.begin():
                    order = await session.get(Order, id)
                    if not order:
                        raise OrderNotFoundError(f"Не найден заказ с ID {id}")
                    
                    if order.status == status.value:
                        logger.warning("Статуса заказа одинаковы")
                    
                    else:
                        order.status = status.value
                        logger.success(f"Изменение статуса заказа на {status.value}")
                    
                    
                    
        except OrderNotFoundError:
            raise
            
        except Exception as e:
            raise