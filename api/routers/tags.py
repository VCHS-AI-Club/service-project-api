from fastapi import APIRouter, Depends, status
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_db
from api.schemas import Tag, TagT

tag_router = APIRouter(prefix="/tags")


@tag_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_tag(id: int, db: AsyncSession = Depends(get_db)):  # noqa
    """Get an item."""
    return await db.get(Tag, id)


@tag_router.get("", status_code=status.HTTP_200_OK)
async def get_all_tags(db: AsyncSession = Depends(get_db)):
    """Get all tags from the db."""
    q = await db.execute(select(Tag).order_by(Tag.id))
    return q.scalars().all()


@tag_router.post("", status_code=status.HTTP_201_CREATED)
async def create_tag(opp: TagT, db: AsyncSession = Depends(get_db)):
    """Put an item."""
    obj = Tag(name=opp.name)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)

    return obj


@tag_router.put("/{id}", status_code=status.HTTP_200_OK)
async def edit_tag(opp: TagT, id: int, db: AsyncSession = Depends(get_db)):  # noqa
    """Edit an item."""
    await db.execute(update(Tag).where(Tag.id == id).values(name=opp.name))
    return await db.get(Tag, id)


@tag_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_tag(id: int, db: AsyncSession = Depends(get_db)):  # noqa
    """Delete an item."""
    await db.execute(delete(Tag).where(Tag.id == id))
