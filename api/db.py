import typing as t

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

__all__ = ("CONNECTION_STRING", "get_db")

CONNECTION_STRING = (
    "postgresql+asyncpg://postgres:postgres@localhost/ai_service_project"
)
engine = create_async_engine(CONNECTION_STRING, echo=True)
SessionLocal = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> t.AsyncIterator[AsyncSession]:
    """`FastAPI` dependency that provides a sqlalchemy session."""
    async with t.cast(AsyncSession, SessionLocal()) as session:
        try:
            yield session
            await session.commit()
        finally:

            await session.close()
