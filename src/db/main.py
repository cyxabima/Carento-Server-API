from src.config import Config
from typing import AsyncGenerator

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


async_engine = create_async_engine(Config.DB_URI, echo=True)


async def init_db():
    async with async_engine.begin() as conn:
        # from src.db.models import Cars

        await conn.run_sync(SQLModel.metadata.create_all)


# this was causing slow response therefore
# You're re-creating the async_sessionmaker every time get_async_session() is called:
AsyncSessionLocal = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get an async database session.
    """

    async with AsyncSessionLocal() as session:
        yield session
