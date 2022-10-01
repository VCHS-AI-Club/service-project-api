from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Opp(Base):
    """Database representation of an opportunity."""

    __tablename__ = "opps"

    id = Column(Integer, primary_key=True, index=True)  # noqa
    name = Column(String, nullable=False)
    desc = Column(String, nullable=False)
    # Location as lat long coordinates
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    # Start and end times as UTC timestamps
    start = Column(Integer, nullable=False)
    end = Column(Integer, nullable=False)


class User(Base):
    """Database representation of a user."""

    __tablename__ = "users"

    id = Column(String, primary_key=True)  # noqa


# Used to validate inputs on api routes
class OppT(BaseModel):
    """Opportunity validation schema."""

    # id: int  # noqa
    name: str
    desc: str
    lat: float
    lon: float
    start: int
    end: int


class UserT(BaseModel):
    """User validation schema."""

    id: str  # noqa
