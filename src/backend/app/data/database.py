from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from data.config import Config
from typing import AsyncGenerator, Generator
from sqlalchemy.orm.session import Session


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    DATABASE_URL = f"mysql+asyncmy://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DATABASE}"
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session


def get_session() -> Generator[Session, None]:
    DATABASE_URL = f"mysql+mysqlconnector://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DATABASE}"
    engine = create_async_engine(DATABASE_URL, echo=True)
    session = sessionmaker(bind=engine)
    with session() as session:
        yield session
