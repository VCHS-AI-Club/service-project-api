from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# UserOppAssociation = Table(
#     "user_opp_association",
#     Base.metadata,
#     Column("user_id", ForeignKey("user.id"), nullable=False, primary_key=True),
#     Column("opp_id", ForeignKey("opp.id"), nullable=False, primary_key=True),
#     Column("rating", Integer),
# )
class UserOppAssociation(Base):
    """Association object for user <-> opp relationship.

    See https://docs.sqlalchemy.org/en/15/orm/basic_relationships.html#association-object
    """

    __tablename__ = "user_opp_association"

    user_id = Column(ForeignKey("user.id"), primary_key=True)
    opp_id = Column(ForeignKey("opp.id"), primary_key=True)
    rating = Column(Integer)
    user = relationship("User", back_populates="opps")
    opp = relationship("Opp", back_populates="users")


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

    opps: "list[Opp]" = relationship("UserOppAssociation", back_populates="user")
    # opps = relationship(
    #     "Opp",
    #     secondary=UserOppAssociation,
    #     back_populates="users",
    # )


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

    users = relationship("UserOppAssociation", back_populates="opp")
    # users = relationship(
    #     "User",
    #     secondary=UserOppAssociation,
    #     back_populates="opps",
    # )


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


class RatingT(BaseModel):
    """Rating type."""

    user_id: str
    rating: int
