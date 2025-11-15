import asyncio
from src.bot.bot import main as run_bot
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


async def main():
    engine = create_async_engine('sqlite+aiosqlite:///db.db')
    Session = async_sessionmaker(engine)
    await run_bot(Session)
    

if __name__ == "__main__":
    asyncio.run(main())