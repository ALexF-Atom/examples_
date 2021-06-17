
from typing import Dict

from app.models import ModelHobby, What, Where, Long, IconState, Icon
from app.models import Background
from app.models import ModelHelper
from app.models.base import db

from sqlalchemy import select, insert


async def all():
    i, ist, h, b = Icon.t, IconState.t, ModelHobby.t, Background.t
    stm = select([h, i,ist, b]).select_from(
        h.join(i.join(ist.join(b)), isouter=True)
    )
    return await db.fetch_all(stm)


async def create(hobby: Dict):
    return await db.execute(ModelHobby.t.insert()
                            .values(**hobby)
                            .returning(ModelHobby.id))


async def delete(hobby_id: int):
    return await db.execute(ModelHobby.t.delete(ModelHobby.id == hobby_id))


async def add_properties(properties: Dict):
    hobby_id = properties['hobby_id']
    what = properties['what']
    where = properties['where']
    long = properties['long']
    id_ = await db.execute(insert(What).values(hobby_id=hobby_id, **what).returning(What.hobby_id))
    assert id_ == hobby_id
    id_ = await db.execute(insert(Where).values(hobby_id=hobby_id, **where).returning(Where.hobby_id))
    assert id_ == hobby_id
    id_ = await db.execute(insert(Long).values(hobby_id=hobby_id, **long).returning(Long.hobby_id))
    assert id_ == hobby_id
    return hobby_id


async def delete_properties(hobby_id: int):
    for model in [What, Where, Long]:
        await db.execute(model.t.delete(model.hobby_id == hobby_id))


async def get_properties(hobby_id: int):
    stm = select([What, Where, Long]).select_from(
        What.t.join(Where, Where.hobby_id == What.hobby_id)
        .join(Long, Long.hobby_id == What.hobby_id))\
        .where(What.hobby_id == hobby_id)
    # stm = select([What, Where, Long]).where(What.hobby_id==hobby_id)\
    # .where(Where.hobby_id==hobby_id)\
    # .where(Long.hobby_id==hobby_id)
    return await db.fetch_one(stm)


async def get_what(hobby_id: int):
    w, h = What.t, ModelHelper.t
    stm = select([w,
            h.c.id.label('helper_id'),
            h.c.text_url_for_helper.label('helper')]).select_from(
                w.join(h, isouter=True)
            ).where(What.hobby_id==hobby_id)
    return await db.fetch_one(stm)


async def get_where(hobby_id: int):
    w, h = Where.t, ModelHelper.t
    stm = select([w,
                  h.c.id.label('helper_id'),
                  h.c.text_url_for_helper.label('helper')]).select_from(
        w.join(h, isouter=True)).where(Where.hobby_id == hobby_id)
    return await db.fetch_one(stm)

async def get_long(hobby_id: int):
    w, h = Long.t, ModelHelper.t
    stm = select([w,
                  h.c.id.label('helper_id'),
                  h.c.text_url_for_helper.label('helper')]).select_from(
        w.join(h, isouter=True)).where(Long.hobby_id == hobby_id)
    return await db.fetch_one(stm)


async def set_what(hobby_id: int, data: Dict):
    return await db.execute(What.t.insert().values(hobby_id=hobby_id, **data))


async def set_where(hobby_id: int, data: Dict):
    return await db.execute(Where.t.insert().values(hobby_id=hobby_id, **data))


async def set_long(hobby_id: int, data: Dict):
    return await db.execute(Long.t.insert().values(hobby_id=hobby_id, **data))
