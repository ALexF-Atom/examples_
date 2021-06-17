from app.models import ModelUserEvent

from typing import Dict, TYPE_CHECKING
import sqlalchemy as sa
from app.models.base import db
from pydantic import UUID4
import datetime
from fastapi.logger import logger

from app.fsm.models import ModelFSM, ModelFSM_Hobby, ModelUserRelationAction, UserNoConfirmEvent
from app.models.event_key import ModelEventKey
if TYPE_CHECKING:
    from app.fsm.user_state_machine import UserStateMachine


from sqlalchemy.dialects.postgresql import insert


async def is_action_in(user_id: UUID4, action_key: int):
    urk = ModelUserRelationAction.t
    stm = sa.select(sa.exists().where(sa.and_(
        urk.c.action_key == action_key,
        urk.c.user_id == user_id
    )))
    return await db.fetch_val(stm)


async def is_closed_event_rule(user_id: UUID4, relation_key: int, key: int):
    urk = ModelUserRelationAction.t
    stm = sa.select(sa.exists().where(sa.and_(
        urk.c.user_id == user_id,
        urk.c.relation_key == relation_key,
        urk.c.key == key
    )))
    return await db.fetch_val(stm)


async def get_closed_event(user_id: UUID4):
    user = ModelUserEvent.t
    return await db.fetch_all(user.select(user.c.user_id == user_id))


async def get_open_app_count_today(user_id: UUID4):
    f = ModelFSM.t
    stm = sa.select([f.c.count_open_app_current_day]).where(
        f.c.user_id == user_id
    )
    return await db.fetch_val(stm)
