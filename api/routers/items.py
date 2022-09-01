
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from api.schemas import Opp, OppT
from api.db import get_db

item_router = APIRouter(prefix="/items")


@item_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_item(id: int, db: AsyncSession = Depends(get_db)):  # noqa
    """Get an item."""
    return await db.get(Opp, id)


@item_router.get("", status_code=status.HTTP_200_OK)
async def get_all_items(db: AsyncSession = Depends(get_db)):
    """Get all items from the db."""
    q = await db.execute(select(Opp).order_by(Opp.id))
    return q.scalars().all()


@item_router.post("", status_code=status.HTTP_201_CREATED)
async def create_item(opp: OppT, db: AsyncSession = Depends(get_db)):
    """Put an item."""
    obj = Opp(name=opp.name, desc=opp.desc)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)

    return obj


@item_router.put("/{id}", status_code=status.HTTP_200_OK)
async def edit_item(opp: OppT, id: int, db: AsyncSession = Depends(get_db)):  # noqa
    """Edit an item."""
    await db.execute(
        update(Opp).where(Opp.id == id).values(name=opp.name, desc=opp.desc)
    )
    return await db.get(Opp, id)


@item_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_item(id: int, db: AsyncSession = Depends(get_db)):  # noqa
    """Delete an item."""
    await db.execute(delete(Opp).where(Opp.id == id))
