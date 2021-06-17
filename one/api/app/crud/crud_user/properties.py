from typing import Any, Dict
from pydantic.types import UUID4

import sqlalchemy as sa
import app.models.user as m
from app.models.hobby import ModelHobby
from app.models.base import db


async def save(user_id: UUID4, user_hobby: Dict) -> int:
    return await db.execute(m.ModelUserSettings.t.insert().values(user_id=user_id, **user_hobby)
                            .returning(m.ModelUserSettings.user_hobby_id))


async def get(user_id: UUID4, user_hobby_id: int) -> m.ModelUserSettings:
    us, uh, h = m.ModelUserSettings.t, m.ModelUserHobby.t, ModelHobby.t
    q = sa.select([h.c.title, uh]).select_from(uh.join(h)).subquery()
    stm = (sa.select([us, q.c.title, q.c.name]).select_from(
        us.join(q, us.c.user_hobby_id == q.c.id))
        .where(us.c.user_hobby_id == user_hobby_id)
        .where(us.c.user_id == user_id))
    return await db.fetch_one(stm)


async def update(user_id: UUID4, user_hobby_id: int, properties_update: Dict) -> int:
    return await db.execute(m.ModelUserSettings.t.update()
                            .where(sa.and_(m.ModelUserSettings.user_hobby_id == user_hobby_id,
                                           m.ModelUserSettings.user_id == user_id))
                            .values(**properties_update)
                            .returning(m.ModelUserSettings.user_hobby_id))



async def get_column(user_id: UUID4, user_hobby_id: int, name: str) -> Any:
    # list(map(lambda x: column(x), columns)
    stm = sa.select(from_obj=m.ModelUserSettings, columns=[sa.column(name)]).where(
        sa.and_(m.ModelUserSettings.user_hobby_id == user_hobby_id,
                m.ModelUserSettings.user_id == user_id))
    return await db.fetch_val(stm)
