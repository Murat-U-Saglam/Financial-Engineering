from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.data.config import Config
from typing import AsyncGenerator, Generator
from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from app.ORM.ticker import Base


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    DATABASE_URL = f"mysql+asyncmy://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DATABASE}"
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session


@contextmanager
def get_session():
    session = None  # Initialize session to None to ensure it's always defined
    DATABASE_URL = f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DATABASE}"
    try:
        engine = create_engine(url=DATABASE_URL, echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
    except SQLAlchemyError as e:
        print(f"Error creating session: {e}")
        raise
    finally:
        if (
            session is not None
        ):  # Check if session was created before attempting to close it
            session.close()


def create_tables():
    DATABASE_URL = f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DATABASE}"
    try:
        engine = create_engine(url=DATABASE_URL, echo=True)
        Base.metadata.create_all(engine)  # Create tables based on your models
        print("All tables created successfully")
    except SQLAlchemyError as e:
        print(f"Error creating tables: {e}")
