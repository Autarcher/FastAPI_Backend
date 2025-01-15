import os
from typing import Callable, AsyncGenerator, Generator
from loguru import logger
from contextlib import contextmanager

from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy_utils import database_exists, create_database

from services.config import AppSettings

def create_db_and_tables(get_settings: Callable[[], AppSettings]):
    logger.info("creating tables ...")
    
    settings: AppSettings = get_settings

    # we'll turn off this verbose logging of queries in production:
    # echo = settings.testing
    echo = True
    # 使用同步engine创建数据库
    engine = create_engine(
        settings.mysql.database_url.replace("mysql+aiomysql", "mysql+pymysql"), echo=echo
    )

    if not database_exists(engine.url):
        create_database(engine.url)


    with engine.begin() as connection:
        SQLModel.metadata.create_all(connection)
    # 使用异步engine进行数据库操作
    return create_async_engine(settings.mysql.database_url, echo=echo), engine


setting = AppSettings()
async_engine, sync_engine = create_db_and_tables(setting)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        async_engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
    
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


def get_sync_session() -> Generator[Session, None, None]:
    sync_session = sessionmaker(
        sync_engine,
        class_=Session,
        expire_on_commit=False
    )
    
    session = sync_session()
    try:
        yield session
    finally:
        session.close()