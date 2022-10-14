from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


UserOppAssociation = Table(
    "user_opp_association",
    Base.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("opp_id", ForeignKey("opp.id")),
)


class Opp(Base):
    """Database representation of an opportunity."""

    __tablename__ = "opp"

    id = Column(Integer, primary_key=True, index=True)  # noqa
    # Basic info
    name = Column(String, nullable=False)
    desc = Column(String, nullable=False)
    isChurch = Column(Boolean, nullable=False)
    contact = Column(String, nullable=True)
    website = Column(String, nullable=True)

    # Location as lat long coordinates
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)

    # Start and end times as UTC timestamps
    start = Column(Integer, nullable=False)
    end = Column(Integer, nullable=False)

    users = relationship(
        "User",
        secondary=UserOppAssociation,
        back_populates="opps",
    )


class User(Base):
    """Database representation of a user."""

    __tablename__ = "user"

    id = Column(String, primary_key=True)  # noqa

    children = Column(Boolean, nullable=True)
    setup_labor = Column(Boolean, nullable=True)
    audio_visual = Column(Boolean, nullable=True)
    teaching = Column(Boolean, nullable=True)
    food = Column(Boolean, nullable=True)
    environment = Column(Boolean, nullable=True)

    opps = relationship(
        "Opp",
        secondary=UserOppAssociation,
        back_populates="users",
        # lazy="joined"
    )


# class UserOppAssociation(Base):
#     """Many to many association table for `Opp` <-> `User` relationship."""
#
#     __tablename__ = "user_opp_association"
#
#     id = Column(Integer, primary_key=True)  # noqa
#     user_id = Column(String, ForeignKey("users.id"))
#     opp_id = Column(Integer, ForeignKey("opps.id"))


# Used to validate inputs on api routes
class OppT(BaseModel):
    """Opportunity validation schema."""

    # id: int  # noqa
    name: str
    desc: str
    contact: str | None
    website: str | None
    isChurch: bool
    lat: float
    lon: float
    start: int
    end: int


class UserT(BaseModel):
    """User validation schema."""

    id: str  # noqa
    children: bool | None
    setup_labor: bool | None
    audio_visual: bool | None
    teaching: bool | None
    food: bool | None
    environment: bool | None
    children: bool | None


class AssociationT(BaseModel):
    """Association request type."""

    user_id: str
    opp_id: int
