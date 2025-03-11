from collections.abc import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import get_settings

settings = get_settings()

SQLALCHEMY_DATABASE_URL = f'sqlite+aiosqlite:///{settings.database_name}'
BASE_SQLALCHEMY_DATABASE_URL = f'sqlite:///{settings.database_name}'


def get_async_engine() -> AsyncEngine:
    return create_async_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True,
    )


AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=get_async_engine(),
    class_=AsyncSession,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


engine = create_engine(BASE_SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
