from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from py_chat.core.config import settings

engine = create_async_engine(
    settings.POSTGRES_URL,
    future=True,
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        try:
            yield session

        except Exception:
            raise
