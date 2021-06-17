from typing import Any, Dict
from pydantic.types import UUID4
import sqlalchemy as sa
from app.schemas.schema_user import SchemaUserAlarmModel
from app.models.user import ModelUserAlarm
from app.models.base import db


async def get(user_id: UUID4, user_hobby_id: int) -> ModelUserAlarm:
    return await db.fetch_one(ModelUserAlarm.t.select().where(ModelUserAlarm.user_hobby_id == user_hobby_id,
                                                      ModelUserAlarm.user_id == user_id))


async def save(user_id: UUID4, data: Dict) -> int:
    return await db.execute(ModelUserAlarm.t.insert().values(user_id=user_id, **data))


async def update(user_id: UUID4, user_hobby_id: int, settings_update: Dict) -> int:
    return await db.execute(ModelUserAlarm.t.update()
                            .where(sa.and_(ModelUserAlarm.user_hobby_id == user_hobby_id,
                                           ModelUserAlarm.user_id == user_id))
                            .values(**settings_update)
                            .returning(ModelUserAlarm.user_hobby_id))


async def get_column(user_id: UUID4, user_hobby_id: int, name: str) -> Any:
    stm = sa.select(from_obj=ModelUserAlarm, columns=[sa.column(name)]).where(
        sa.and_(ModelUserAlarm.user_hobby_id == user_hobby_id,
                ModelUserAlarm.user_id == user_id))
    return await db.fetch_val(stm)
