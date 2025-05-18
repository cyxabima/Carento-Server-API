from src.config import Config
from typing import AsyncGenerator

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


async_engine = create_async_engine(
    Config.DB_URI,
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # this line!  Important for Neon
)


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


# Notes:=> for the parameters used in async engine

# pool_size: This determines the initial number of database connections
# that SQLAlchemy will maintain in its connection pool.
# In this case, SQLAlchemy will start with 10 connections ready to be used.

# max_overflow: This setting controls how many additional connections SQLAlchemy
# can create beyond the pool_size if all the existing connections are in use.
# Here, if all 10 connections are busy, SQLAlchemy can create up to 20 more
# connections to handle the extra load.

# pool_pre_ping:  This is crucial for Neon.  When set to True, SQLAlchemy will test
# the validity of a connection before it's used from the pool.
# If Neon (or any database) has closed an idle connection, SQLAlchemy will detect
# this and transparently recycle the connection (i.e., create a new one) instead of
# your application getting a "connection closed" error.
