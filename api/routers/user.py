from fastapi import APIRouter, Depends
from sqlalchemy import and_, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from api.db import get_db
from api.schemas import AssociationT, Opp, OppT, User, UserOppAssociation, UserT

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
):
    """Get the opps that a user joined."""

    user: User
    user = (
        await db.execute(
            select(User)
            .where(User.id == id)
            .options(
                selectinload(User.opp_association).subqueryload(UserOppAssociation.opp),
            )
        )
    ).scalar()
    print(user.opps)
    # TODO: Fix recursion error: change assoc_proxy to viewonly relationship
    return [
        {
            "name": o.name,
            "id": o.id,
            "desc": o.desc,
            "isChurch": o.isChurch,
            "contact": o.contact,
            "website": o.website,
            "lat": o.lat,
            "lon": o.lon,
            "start": o.start,
            "end": o.end,
            "rating": a.rating,
        }
        for o, a in zip(user.opps, user.opp_association)
    ]


@user_router.get("/{id}/inverse_opps")
async def get_user_inverse_opps(
    id: str,  # noqa
    db: AsyncSession = Depends(get_db),
):
    """Get the opps that a user has not joined."""

    inverse_opp_associations = (
        await db.execute(
            select(Opp).where(
                Opp.id.not_in(
                    (
                        await db.execute(
                            select(UserOppAssociation.opp_id).where(
                                UserOppAssociation.user_id == id
                            )
                        )
                    ).scalars()
                )
            )
        )
    ).scalars()
    return list(inverse_opp_associations)


@user_router.post("/opp")
async def add_opp(asc: AssociationT, db: AsyncSession = Depends(get_db)):  # noqa
    """Add an opp to a user."""
    await db.merge(UserOppAssociation(user_id=asc.user_id, opp_id=asc.opp_id))
    # asc = UserOppAssociation(user_id=asc.user_id, opp_id=asc.opp_id)
    # print(asc)
    # await db.merge(asc)


@user_router.delete("/{user_id}/opp/{opp_id}")
async def remove_opp(user_id: str, opp_id: int, db: AsyncSession = Depends(get_db)):
    """Remove an opp from a user."""
    print("removing opp")
    opp = (
        await db.execute(
            select(UserOppAssociation).where(
                (UserOppAssociation.user_id == user_id)
                & (UserOppAssociation.opp_id == opp_id)
            )
        )
    ).scalar()
    print("opp", opp)
    await db.execute(
        delete(UserOppAssociation).where(
            (UserOppAssociation.user_id == user_id)
            & (UserOppAssociation.opp_id == opp_id)
        )
    )
    return opp
