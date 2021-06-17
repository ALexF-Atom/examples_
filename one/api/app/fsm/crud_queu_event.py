import sqlalchemy as sa
from app.models.base import db
from pydantic import UUID4
from app.fsm.models import ModelUserRelationAction, UserNoConfirmEvent



from sqlalchemy.dialects.postgresql import insert


async def all_last_event_key(user_id: UUID4):
    une = UserNoConfirmEvent.t
    stm = sa.select([une.c.event_id]).where(une.c.user_id == user_id)
    return await db.fetch_all(stm)


async def add_last_event_key(user_id: UUID4, event_id: int):
    une = UserNoConfirmEvent.t
    stm = insert(une).values(user_id=user_id, event_id=event_id)
    stm_update_insert = stm.on_conflict_do_update(
        constraint='unique_lost_event',
        set_=dict(user_id=user_id, event_id=event_id))
    return await db.execute(stm_update_insert)


async def get_last_event_key(user_id: UUID4):
    une = UserNoConfirmEvent.t
    stm = sa.select([une.c.event_id]).where(une.c.user_id == user_id).limit(1)
    return await db.fetch_val(stm)


async def is_exists_key_in_last(user_id: UUID4, event_id: int):
    une = UserNoConfirmEvent.t
    stm = sa.select(sa.exists().where(sa.and_(une.c.user_id == user_id,
                                      une.c.event_id == event_id)))
    return await db.fetch_val(stm)


async def delete_last_event_key(user_id: UUID4, event_id: int):
    une = UserNoConfirmEvent.t
    stm = une.delete().where(sa.and_(une.c.user_id == user_id,
                                     une.c.event_id == event_id))
    return await db.execute(stm)


