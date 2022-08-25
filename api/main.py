#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""Entry point for the api."""
import typing as t
from functools import lru_cache
from uuid import UUID

from fastapi import Depends, FastAPI
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from fastapi_utils.session import FastAPISessionMaker
from pydantic import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class Opp(Base):
    """Database representation of an opportunity."""

    __tablename__ = "opps"

    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)  # noqa
    name = Column(String, nullable=False)
    desc = Column(String, nullable=False)


# Used to validate inputs on api routes
class OppT(BaseModel):
    """Opportunity type."""

    id: UUID  # noqa
    name: str
    desc: str


def get_db() -> t.Iterator[Session]:
    """`FastAPI` dependency that provides a sqlalchemy session."""
    yield from _get_fastapi_sessionmaker().get_db()


@lru_cache()
def _get_fastapi_sessionmaker() -> FastAPISessionMaker:
    return FastAPISessionMaker("sqlite+pysqlite:///databasae.sqlite3")


app = FastAPI()


@app.get("/items/{id_}")
async def get_item(db: Session = Depends(get_db), *, id_: UUID):
    """Get an item."""
    return db.query(Opp).get(id_)


@app.get("/items/")
async def get_all_items(db: Session = Depends(get_db)):
    """Get all items from the db."""
    return db.query(Opp).all()


@app.post("/items/")
async def create_item(opp: OppT, db: Session = Depends(get_db)):
    """Put an item."""
    obj = Opp(id=opp.id, name=opp.name, desc=opp.desc)
    db.add(obj)
    db.flush()
    return obj
