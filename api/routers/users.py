from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.schemas import UserT, User
from api.db import get_db

user_router = APIRouter(prefix="/users")

@user_router.post("")
def create_user(user: UserT, db: AsyncSession = Depends(get_db)):
    """Create a user"""
    u = User(id=user.id)
    db.add(u)
    return u


@user_router.get("")
async def get_all_uesrs(db: AsyncSession = Depends(get_db)):
    """Get all users."""
    q = await db.execute(select(User).order_by(User.id))
    return q.scalars().all()

@user_router.get("/{id}")
async def get_user(id: str, db: AsyncSession = Depends(get_db)):
    """Get a user by id."""
    return await db.get(User, id)
