__all__ = [
    "ProductManager"
]
from typing import Optional, List, Tuple

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from loguru import logger

from ..core import Product
from ..core.exceptions import ProductNotFoundError
from ..schemas.product import ProductCreateSchema, ProductUpdateSchema, ProductSchema

class ProductManager:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.Session = session_maker
        logger.debug("Инициализирован ProductManager")
        
    async def create_product(self, product_data: ProductCreateSchema) -> ProductSchema:
        """Создать продукт"""
        logger.info(f"🆕 Создание продукта: '{product_data.title}'")
        logger.debug(f"Данные продукта: {product_data.model_dump()}")
        
        try:
            async with self.Session() as session:
                async with session.begin():
                    product = Product(**product_data.model_dump())
                    session.add(product)
                    await session.flush()
                    
                    logger.success(
                        f"✅ Продукт создан: '{product_data.title}' "
                        f"(ID: {product.id}, Цена: {product.price}, Кол-во: {product.count})"
                    )
                    return ProductSchema(**product.as_dict())
                    
        except Exception as e:
            logger.error(
                f"❌ Ошибка создания продукта '{product_data.title}': {str(e)}"
            )
            raise
    
    async def get_product(self, id: int) -> Optional[ProductSchema]:
        """Получение продукта"""
        logger.info(f"🔍 Поиск продукта ID: {id}")
        
        try:
            async with self.Session() as session:
                product = await session.get(Product, id)
                
                if product:
                    logger.info(
                        f"✅ Найден продукт: '{product.title}' "
                        f"(ID: {product.id}, Цена: {product.price}, В наличии: {product.count})"
                    )
                else:
                    logger.warning(f"⚠️ Продукт ID: {id} не найден")
                    
                return ProductSchema(**product.as_dict()) if product else None
                
        except Exception as e:
            logger.error(f"❌ Ошибка поиска продукта ID: {id}: {str(e)}")
            raise
        
    async def update_product(self, product_data: ProductUpdateSchema) -> ProductSchema:
        """Обновление продукта"""
        logger.info(f"🔄 Обновление продукта ID: {product_data.id}")
        logger.debug(f"Данные для обновления: {product_data.model_dump(exclude_unset=True)}")
        
        try:
            async with self.Session() as session:
                async with session.begin():
                    product = await session.get(Product, product_data.id)
                    if not product:
                        logger.error(f"❌ Продукт ID: {product_data.id} не найден для обновления")
                        raise ProductNotFoundError(f"Продукт {product_data.id} не найден")
                    
                    update_data = product_data.model_dump(exclude_unset=True, exclude_none=True)
                    changes = []
                    
                    for field, value in update_data.items():
                        old_value = getattr(product, field)
                        if old_value != value:
                            setattr(product, field, value)
                            changes.append(f"{field}: {old_value} → {value}")
                    
                    if changes:
                        logger.info(
                            f"✅ Обновлен продукт ID: {product_data.id} "
                            f"('{product.title}'). Изменения: {', '.join(changes)}"
                        )
                    else:
                        logger.info(f"ℹ️ Продукт ID: {product_data.id} не требует изменений")
                    
                    return ProductSchema(**product.as_dict())
                    
        except ProductNotFoundError:
            raise
        
        except Exception as e:
            logger.error(f"❌ Ошибка обновления продукта ID: {product_data.id}: {str(e)}")
            raise
    
    async def delete_product(self, id: int) -> Tuple[bool, str]:
        """Удаление продукта"""
        logger.info(f"🗑️ Удаление продукта ID: {id}")
        
        try:
            async with self.Session() as session:
                async with session.begin():
                    product = await session.get(Product, id)
                    if not product:
                        logger.warning(f"⚠️ Продукт ID: {id} не найден для удаления")
                        return False, f"Продукт ID: {id} не найден для удаления"
                    
                    product_title = product.title
                    await session.delete(product)
                    
                    logger.success(f"✅ Удален продукт: '{product_title}' (ID: {id})")
                    return True, f"Удален продукт: '{product_title}' (ID: {id})"
                
        except Exception as e:
            logger.error(f"❌ Ошибка удаления продукта ID: {id}: {str(e)}")
            raise
    
    async def get_all_products(self) -> List[ProductSchema]:
        """Получение всех продуктов"""
        logger.info("📋 Получение списка всех продуктов")
        
        try:
            async with self.Session() as session:
                result = await session.execute(select(Product))
                products = result.scalars().all()
                
                logger.info(f"📊 Загружено продуктов: {len(products)}")
                return [ProductSchema(**x.as_dict()) for x in products]
                
        except Exception as e:
            logger.error(f"❌ Ошибка получения списка продуктов: {str(e)}")
            raise
        
    async def get_products(self, order_ids: List[int]) -> List[ProductSchema]:
        """Получить несколько заказов с продуктами (1 запрос)"""
        
        async with self.Session() as session:
            stmt = (
                select(Product)
                .where(Product.id.in_(order_ids))
                .order_by(Product.id)
            )
            result = await session.execute(stmt)
            orders = result.scalars().all()
            
            return [ProductSchema(**order.as_dict()) for order in orders]