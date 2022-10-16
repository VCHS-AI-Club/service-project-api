from fastapi import APIRouter, Depends
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.db import get_db
from api.schemas import (AssociationT, Opp, OppT, User, UserOppAssociation,
                         UserT)

user_router = APIRouter(prefix="/user")


@user_router.post("")
def create_user(user: UserT, db: AsyncSession = Depends(get_db)):
    """Create a user."""
    u = User(id=user.id)
    db.add(u)
    return u


@user_router.get("")
async def get_all_uesrs(db: AsyncSession = Depends(get_db)):
    """Get all users."""
    q = await db.execute(select(User).order_by(User.id))
    return q.scalars().all()


@user_router.get("/{id}")
async def get_user(id: str, db: AsyncSession = Depends(get_db)):  # noqa
    """Get a user by id."""
    return await db.get(User, id)


@user_router.post("")
async def create_uesr(user: UserT, db: AsyncSession = Depends(get_db)) -> User:
    """Create a user."""
    obj = User(**dict(user))
    db.add(obj)
    await db.commit()
    await db.refresh(obj)

    return obj


@user_router.put("/{id}")
async def edit_user(user: UserT, id: str, db: AsyncSession = Depends(get_db)):  # noqa
    """Edit a user."""
    # await db.execute(update(User).where(User.id == id).values(**dict(user)))
    await db.merge(User(**dict(user)))
    await db.commit()
    return await db.get(User, user.id)


@user_router.delete("/{id}")
async def delete_user(id: str, db: AsyncSession = Depends(get_db)):  # noqa
    """Delete a user."""
    await db.execute(delete(User).where(User.id == id))


@user_router.get("/{id}/opps")
async def get_user_opps(
    id: str,  # noqa
    db: AsyncSession = Depends(get_db),
) -> list[Opp]:
    """Get the opps that a user joined."""

    user: User
    user = (
        await db.execute(
            select(User)
            .where(User.id == id)
            .options(
                selectinload(User.opp_association)
                .subqueryload(UserOppAssociation.opp),
            )
        )
    ).scalar()
    # TODO: Fix recursion error: change assoc_proxy to viewonly relationship

@user_router.post("/opp")
async def add_opp(asc: AssociationT, db: AsyncSession = Depends(get_db)):  # noqa
    """Add an opp to a user."""
    await db.merge(UserOppAssociation(user_id=asc.user_id, opp_id=asc.opp_id))
    # asc = UserOppAssociation(user_id=asc.user_id, opp_id=asc.opp_id)
    # print(asc)
    # await db.merge(asc)
