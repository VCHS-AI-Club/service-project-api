import os
import typing as t
from urllib.parse import urlparse
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

__all__ = ("CONNECTION_STRING", "get_db", "format_db_url")


def format_db_url(url_str: str):
    """Format the default cockroachdb connection string to the sqlalchemy-cockroach format.

    ---
    cockroachdb[+driver]://<username>:<password>@cockroachlabs.cloud:<port>/<database>?sslmode=verify-full&options=--cluster%3D<cluster_id>

    cockroachdb+asyncpg://<username>:<password>@cockroachlabs.cloud:<port>/<cluster_id>.<database>
    """
    # base url inlcuding top lvl domain
    url = urlparse(url_str)
    cluster_id = url.query.split("--cluster%3D")[1]
    return f"{url.scheme}://{url.netloc}/{cluster_id}.{url.path[1:]}"


DEPLOYMENT = os.getenv("DEPLOYMENT", "DEV")
CONNECTION_STRING = format_db_url(os.getenv(f"{DEPLOYMENT}_DATABASE_URL", ""))

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
