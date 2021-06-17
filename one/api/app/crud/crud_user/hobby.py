from re import L
from typing import Iterable, NoReturn
from pydantic import UUID4
from databases.backends.postgres import Record

import sqlalchemy as sa
from app.models import ModelUser, ModelUserHobby, ModelHobby, ModelUserSettings
from app.models.base import db


async def get(user_id: UUID4) -> Iterable[Record]:
    u, h, uh = ModelUser.t, ModelHobby.t, ModelUserHobby.t
    stm = sa.select([h, uh.c.id.label('user_hobby_id'), uh.c.name.label('user_hobby_name')]).select_from(
        uh.outerjoin(u, u.c.uid == uh.c.user_id).
        outerjoin(h, h.c.id == uh.c.hobby_id)
    ).where(u.c.uid == user_id)
    return await db.fetch_all(stm)


async def get_user_hobby_id(user_id: UUID4, hobby_id: int):
    stm = sa.select([ModelUserHobby.id]).where(ModelUserHobby.user_id == user_id,
                                               ModelUserHobby.hobby_id == hobby_id)
    return await db.fetch_val(stm)


async def count(user_id: UUID4):
    stm = sa.select([sa.func.count()]).select_from(
        ModelUserHobby).where(ModelUserHobby.user_id == user_id)
    return await db.fetch_val(stm)


async def get_user_hobby(user_hobby_id: int):
    h, uh, us = ModelHobby.t, ModelUserHobby.t, ModelUserSettings.t
    stm = sa.select([h.c.title,
                     uh.c.id.label('user_hobby_id'),
                     uh.c.name.label('user_hobby_name'),
                     us.c.what,
                     us.c.where,
                     us.c.long]).select_from(
        uh.join(h).join(us)
    ).where(uh.c.id == user_hobby_id)
    return await db.fetch_one(stm)


async def delete(user_id: UUID4, user_hobby_id: int) -> NoReturn:
    return await db.execute(ModelUserHobby.t.delete().where(
        ModelUserHobby.id == user_hobby_id,
        ModelUserHobby.user_id == user_id
    ))


async def save(user_id: UUID4, hobby_id: int) -> int:
    return await db.execute(ModelUserHobby.t.insert().values(user_id=user_id, hobby_id=hobby_id)
                            .returning(ModelUserHobby.id))


async def auth_is_user_hobby_id(user_id: UUID4, user_hobby_id: int) -> bool:
    uh = ModelUserHobby.t
    stm = sa.select(sa.exists().where(sa.and_(uh.c.user_id == user_id,
                                              uh.c.id == user_hobby_id)))
    return await db.fetch_val(stm)
