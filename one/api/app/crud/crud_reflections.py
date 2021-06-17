from app.models.user import ModelUserHobby
from app.models.reflections import (ModelReflections,
                                    ModelReflectionsLevel,
                                    ModelComplexity,
                                    ModelLevelScript,
                                    ModelReflectionsFinal)
from app.models import Background
from app.models.base import db
import sqlalchemy as sa
from typing import Dict, List


async def get(user_hobby_id: int):
    uh, r, rl, c = ModelUserHobby.t, ModelReflections.t, ModelReflectionsLevel.t, ModelComplexity.t
    bg = Background.t
    stm = sa.select([r.c.title.label('text'),
                     r.c.hobby_id,
                     rl.c.script_level_id.label('script'), c,
                     bg.c.colors.label('background_colors'),
                     bg.c.vector.label('background_vector')]).select_from(
        r.outerjoin(uh, uh.c.hobby_id == r.c.hobby_id)
        .join(rl)
        .join(c)
        .outerjoin(bg, bg.c.id == c.c.background_id)
    ).where(uh.c.id == user_hobby_id)
    return await db.fetch_all(stm)


async def get_title(script_id: int):
    return await db.fetch_one(sa.select([ModelLevelScript]).where(ModelLevelScript.id == script_id))


async def get_final(final_id: int):
    return await db.fetch_one(sa.select([ModelReflectionsFinal]).where(ModelReflectionsFinal.id == final_id))


async def save_final(data: Dict):
    return await db.execute(sa.insert(ModelReflectionsFinal)
                            .values(**data)
                            .returning(ModelReflectionsFinal.id))


async def get_id_script(user_hobby_id: int):
    uh, r = ModelUserHobby.t, ModelReflections.t,
    stm = sa.select([r.c.script_id]).select_from(
        r.outerjoin(uh, uh.c.hobby_id == r.c.hobby_id)
    ).where(uh.c.id == user_hobby_id)
    return await db.fetch_val(stm)
