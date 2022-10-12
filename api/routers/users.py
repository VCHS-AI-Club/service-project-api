from fastapi import APIRouter, Depends
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_db
from api.schemas import Opp, OppT, User, UserT

user_router = APIRouter(prefix="/users")


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
async def create_uesr(user: UserT, db: AsyncSession = Depends(get_db)):
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


@user_router.post("/{user_id}/{opp_id}")
async def add_opp(
    user_id: str, opp_id: int, db: AsyncSession = Depends(get_db)
):  # noqa
    """Add an opp to a user."""

    # q = await db.execute(select(User).where(User.id == user_id))
    # user = q.scalars().all()
    # user.opps.append(Opp(id=opp_id))
    # TODO: figure this out


@user_router.delete("/{id}")
async def delete_user(id: str, db: AsyncSession = Depends(get_db)):  # noqa
    """Delete a user."""
    await db.execute(delete(User).where(User.id == id))
