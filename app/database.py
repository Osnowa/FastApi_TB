from typing import Annotated

from fastapi import Depends

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import Config

config = Config.from_env()

engine = create_async_engine(
    config.DATABASE_URL,
    echo = False
)

SessionFactory = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def create_table():
    '''Создание таблиц в базе данных'''
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def disponse_engine():
    '''Закрытие соединения с базой данных'''
    await engine.dispose()

async def get_session():
    '''Получение сессии для работы с базой данных'''
    async with SessionFactory() as session:
        yield session

# Аннотация, что бы не писать SessionDep = Depends(get_session) в каждом эндпоинте
SessionDep = Annotated[AsyncSession, Depends(get_session)]