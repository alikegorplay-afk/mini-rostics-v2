from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from fastapi import FastAPI
from .routers import create


def create_app(sessionmaker: async_sessionmaker[AsyncSession]) -> FastAPI:
    app = FastAPI()
    for router in create(sessionmaker):
        app.include_router(router)
    
    return app