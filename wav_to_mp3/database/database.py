"""Соединение и работа с базой данных."""
import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = os.getenv("POSTGRES_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """ Базовый класс для ORM моделей данных. """


async def init_db() -> None:
    """ Инициализация таблиц БД на основании ORM моделей. """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def shutdown_db() -> None:
    """ Завершение работы с БД. """
    await engine.dispose()
