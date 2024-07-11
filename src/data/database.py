from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from data.config import Config
from typing import AsyncGenerator


# Create a new Async Engine instance


# Create a configured "Session" class


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    DATABASE_URL = f"mysql+asyncmy://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DATABASE}"
    print(DATABASE_URL)
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session
