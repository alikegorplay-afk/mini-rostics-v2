import asyncio
import os

from src.frontend import get_router
from src.api import create_app
from src.bot.bot import main as run_bot
from src.core.database.models import Base
from src.core.const import DATABASE_URL

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from fastapi.staticfiles import StaticFiles
from loguru import logger

import uvicorn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "src", "frontend", "static")


async def main():
    for path in ["data", "data/database", "data/img"]:
        try:
            os.mkdir(path)
        except Exception as e:
            continue
        
    engine = create_async_engine(DATABASE_URL)
    Session = async_sessionmaker(engine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    app = create_app(Session)
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
        
    app.include_router(get_router(Session))
    config = uvicorn.Config(app, "0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await asyncio.gather(
        run_bot(Session),
        server.serve()
    )
    

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Программа остоновлена пользователем")
    except Exception as e:
        logger.critical(f"Неизваестная ошибка! Программа остонавливается: (error = {e})")