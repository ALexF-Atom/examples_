from asyncpg.exceptions import DataError
from app.fsm.schema import FSM_APP, FSM_Hobby
from fastapi.logger import logger
from pydantic import UUID4
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

from app.models.base import db
from app.fsm.models import ModelFSM, ModelFSM_Hobby, ModelUserRelationAction
from app.models import ModelUserEvent

if TYPE_CHECKING:
    from app.fsm.user_state_machine import UserStateMachine


async def update_state_app(user: 'UserStateMachine'):
    stm = (ModelFSM.t.update().values(**dict(user.app))
           .where(ModelFSM.user_id == user.user_id))
    return await db.execute(stm)


async def update_state_routine(user: 'UserStateMachine'):
    stm = sa.update(ModelFSM_Hobby).values(**dict(user.hobby)).where(
        sa.and_(ModelFSM_Hobby.user_id == user.user_id,
                ModelFSM_Hobby.user_hobby_id == user.user_hobby_id))
    return await db.execute(stm)


async def if_user_routine(user_id: UUID4, user_hobby_id: int):
    stm = sa.select(sa.exists().where(
        sa.and_(ModelFSM_Hobby.user_id == user_id,
                ModelFSM_Hobby.user_hobby_id == user_hobby_id)))
    return await db.fetch_val(stm)


async def if_user_app(user_id: UUID4):
    stm = sa.select(sa.exists().where(ModelFSM.user_id == user_id))
    return await db.fetch_val(stm)


async def update_last_hobby(user_id: UUID4, user_hobby_id: int):
    stm = ModelFSM.t.update().values(current_hobby_id=user_hobby_id).where(
        ModelFSM.user_id == user_id)
    return await db.execute(stm)


async def get_current_hobby(user_id: UUID4):
    fsm = ModelFSM.t
    stm = sa.select([fsm.c.current_hobby_id]).where(
        fsm.c.user_id == user_id)
    return await db.fetch_val(stm)


async def create_state_app(**data):
    fsm = ModelFSM.t
    if await if_user_app(data['user_id']):
        stm = sa.update(fsm).values(**data).where(sa.and_(
            *(sa.column(key) == value
              for key, value in data.items())
        )).returning(fsm.c.user_id)
    else:
        stm = sa.insert(fsm).values(**data).returning(fsm.c.user_id)
    return await db.execute(stm)


async def create_state_routine(**data):
    fsm = ModelFSM_Hobby.t
    if await if_user_routine(data['user_id'], data['user_hobby_id']):
        stm = sa.update(fsm).values(**data).where(sa.and_(
            *(sa.column(key) == value
              for key, value in data.items())
        )).returning(fsm.c.id)
    else:
        stm = sa.insert(fsm).values(**data).returning(fsm.c.id)
    return await db.execute(stm)


async def save_action(user_id: UUID4, action_key: int, related_name: str, key_id: int):
    
    urk = ModelUserRelationAction.t
    stm = sa.insert(urk).values(user_id=user_id,
                              action_key=action_key,
                              related_name=related_name,
                              key_id=key_id)
  
    return await db.execute(stm)
    


async def get_current_event_key(user_id: UUID4):
    fsm = ModelFSM.t
    stm = sa.select([fsm.c.event_key]).where(fsm.c.user_id == user_id)
    return await db.fetch_val(stm)


async def set_current_event_key(user_id: UUID4, event_id: int):
    fsm = ModelFSM.t
    stm = fsm.update().values(event_key=event_id).where(fsm.c.user_id == user_id)
    return await db.execute(stm)


async def closing_level_event(user_id: UUID4, event_id: int, user_hobby_id: int):
    user = ModelUserEvent.t
    stm = user.insert().values(user_id=user_id,
                               event_id=event_id,
                               user_hobby_id=user_hobby_id)
    return await db.execute(stm)


async def get_state_level_info(user_id: UUID4):
    fsm = ModelFSM.t
    stm = sa.select([fsm.c.current_level.label('stage'),
                     fsm.c.progress_level.label('progress')]).where(fsm.c.user_id == user_id)
    return await db.fetch_one(stm)


async def current_state_app(user_id: UUID4):
    fsm = ModelFSM.t
    stm = sa.select([fsm]).where(fsm.c.user_id == user_id)
    return await db.fetch_one(stm)


async def current_state_routine(user_id: UUID4, user_hobby_id: int):
    fsm = ModelFSM_Hobby.t
    stm = sa.select([fsm]).where(sa.and_(fsm.c.user_id == user_id,
                                         fsm.c.user_hobby_id==user_hobby_id))
    return await db.fetch_one(stm)
