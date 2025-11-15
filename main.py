import asyncio
from src.api import create_app
from src.bot.bot import main as run_bot
from src.core.database.models import Base
from src.core.const import DATABASE_URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import uvicorn

async def main():
    engine = create_async_engine(DATABASE_URL)
    Session = async_sessionmaker(engine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    app = create_app(Session)
    config = uvicorn.Config(app, "0.0.0.0", 8000)
    server = uvicorn.Server(config)
    await asyncio.gather(
        run_bot(Session),
        server.serve()
    )
    

if __name__ == "__main__":
    asyncio.run(main())