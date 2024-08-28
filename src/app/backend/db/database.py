from backend.db.config import Config
from backend.models.SQLModel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from typing import AsyncGenerator


DATABASE_URL = Config.DATABASE_URL

engine = create_async_engine(url=DATABASE_URL, echo=True, future=True)


SessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession, future=True
)


async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
