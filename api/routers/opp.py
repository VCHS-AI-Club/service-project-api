from fastapi import APIRouter, Depends, status
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_db
from api.schemas import Opp, OppT, RatingT, UserOppAssociation

opp_router = APIRouter(prefix="/opp")


@opp_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_opp(id: int, db: AsyncSession = Depends(get_db)):  # noqa
    """Get an opps"""
    return await db.get(Opp, id)


@opp_router.get("", status_code=status.HTTP_200_OK)
async def get_all_opps(db: AsyncSession = Depends(get_db)):
    """Get all opps from the db."""
    q = await db.execute(select(Opp).order_by(Opp.id))
    return q.scalars().all()


@opp_router.post("", status_code=status.HTTP_201_CREATED)
async def create_opp(opp: OppT, db: AsyncSession = Depends(get_db)):
    """Put an opp."""
    obj = Opp(**dict(opp))
    db.add(obj)
    await db.commit()
    await db.refresh(obj)

    return obj


@opp_router.put("/{id}", status_code=status.HTTP_200_OK)
async def edit_opp(opp: OppT, id: int, db: AsyncSession = Depends(get_db)):  # noqa
    """Edit an opp."""
    await db.execute(update(Opp).where(Opp.id == id).values(**dict(opp)))
    return await db.get(Opp, id)


@opp_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_opp(id: int, db: AsyncSession = Depends(get_db)):  # noqa
    """Delete an opp."""
    await db.execute(delete(Opp).where(Opp.id == id))


@opp_router.post("/{id}/rate")
async def rate_opp(
    rating: RatingT,
    id: int,  # noqa
    db: AsyncSession = Depends(get_db),
):
    """Rate an opp."""
    await db.execute(
        update(UserOppAssociation)
        .where(
            UserOppAssociation.user_id == rating.user_id
            and UserOppAssociation.opp_id == id
        )
        .values(rating=rating.rating)
    )
