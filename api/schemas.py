from pydantic import BaseModel
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Opp(Base):
    """Database representation of an opportunity."""

    __tablename__ = "opps"

    id = Column(Integer, primary_key=True, index=True)  # noqa
    name = Column(String, nullable=False)
    desc = Column(String, nullable=False)


association_table = Table(
    "association",
    Base.metadata,
    Column("tag_id", ForeignKey("tags.id")),
    Column("user_id", ForeignKey("users.id")),
)


class Tag(Base):
    """Database representation of a tag."""

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)  # noqa
    name = Column(String, nullable=False)


class User(Base):
    """Database representation of a user."""

    __tablename__ = "users"

    id = Column(String, primary_key=True)  # noqa
    tags = relationship("Tag", secondary=association_table)


# Used to validate inputs on api routes
class OppT(BaseModel):
    """Opportunity validation schema."""

    # id: int  # noqa
    name: str
    desc: str


class UserT(BaseModel):
    """User validation schema."""

    id: str  # noqa


class TagT(BaseModel):
    """Tag validation schema."""

    name: str
