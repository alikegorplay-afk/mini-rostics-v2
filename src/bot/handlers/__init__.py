from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from .start import router as start_router
from .product import product_api_router
from .create_product import product_add_router
from .order import init_order_router

def init(session_maker: async_sessionmaker[AsyncSession]):
    product_router = product_add_router(session_maker)
    product_api = product_api_router(session_maker)
    order = init_order_router(session_maker)
    return [start_router, product_api, product_router, order]