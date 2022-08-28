#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""Entry point for the api."""
import typing as t

from fastapi import Depends, FastAPI, status
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Opp(Base):
    """Database representation of an opportunity."""

    __tablename__ = "opps"

    id = Column(Integer, primary_key=True, index=True)  # noqa
    name = Column(String, nullable=False)
    desc = Column(String, nullable=False)


class Tag(Base):
    """Database representation of a tag."""

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)  # noqa
    name = Column(String, nullable=False)


# Used to validate inputs on api routes
class OppT(BaseModel):
    """Opportunity type."""

    # id: int  # noqa
    name: str
    desc: str


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


app = FastAPI()


@app.get("/items/{id}", status_code=status.HTTP_200_OK)
async def get_item(id: int, db: AsyncSession = Depends(get_db)):  # noqa
    """Get an item."""
    return await db.get(Opp, id)


@app.get("/items/", status_code=status.HTTP_200_OK)
async def get_all_items(db: AsyncSession = Depends(get_db)):
    """Get all items from the db."""
    q = await db.execute(select(Opp).order_by(Opp.id))
    return q.scalars().all()


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(opp: OppT, db: AsyncSession = Depends(get_db)):
    """Put an item."""
    obj = Opp(name=opp.name, desc=opp.desc)
    db.add(obj)
    await db.flush()
    return obj


@app.put("/items/{id}", status_code=status.HTTP_200_OK)
async def edit_item(opp: OppT, id: int, db: AsyncSession = Depends(get_db)):  # noqa
    """Edit an item."""
    await db.execute(
        update(Opp).where(Opp.id == id).values(name=opp.name, desc=opp.desc)
    )
    return await db.get(Opp, id)


@app.delete("/items/{id}", status_code=status.HTTP_200_OK)
async def delete_item(id: int, db: AsyncSession = Depends(get_db)):  # noqa
    """Delete an item."""
    await db.execute(delete(Opp).where(Opp.id == id))
