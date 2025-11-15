from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from .start import router as start_router
from .scan import router as scan_router
from .tool import router as help_router
from .create_product import product_add_router

def init(session_maker: async_sessionmaker[AsyncSession]):
    product_router = product_add_router(session_maker)
    return [start_router, scan_router, help_router, product_router]