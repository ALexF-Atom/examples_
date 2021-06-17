import datetime
from typing import Dict
from pydantic.types import UUID4
import sqlalchemy as sa


from app.models.user import ModelUserHistory, ModelUserReflectionDay, ModelUserReflectionHistory
from app.models.base import db


async def save_hobby(user_id: UUID4, history: Dict) -> int:
    return await db.execute(ModelUserHistory.t.insert().values(user_id=user_id, **history)
                            .returning(ModelUserHistory.id))


async def save_reflections(user_id: UUID4, history: Dict) -> int:
    return await db.execute(ModelUserReflectionHistory.t.insert().values(user_id=user_id, **history)
                            .returning(ModelUserReflectionHistory.id))


async def save_reflections_day(user_id: UUID4, history: Dict) -> int:
    return await db.execute(ModelUserReflectionDay.t.insert().values(user_id=user_id, **history)
                            .returning(ModelUserReflectionDay.id))


async def get_spent_time(user_id: UUID4, user_hobby_id: int, date: datetime.date):
    stm = sa.select([ModelUserHistory.spent_time]).where(ModelUserHistory.user_hobby_id == user_hobby_id,
                                                         ModelUserHistory.user_id == user_id,
                                                         ModelUserHistory.date == date)
    return await db.fetch_val(stm)


async def get_total_day_spent_time(user_id: UUID4, user_hobby_id: int, date: datetime.date):
    uh = ModelUserHistory.t
    stm = sa.select([sa.func.coalesce(sa.func.sum(uh.c.spent_time), 0)]).where(ModelUserHistory.user_hobby_id == user_hobby_id,
                                                                               ModelUserHistory.user_id == user_id,
                                                                               ModelUserHistory.date == date)
    return await db.fetch_val(stm)


async def get_last_spent_time(user_id: UUID4, user_hobby_id: int, date: datetime.date):
    stm = sa.select([ModelUserHistory.spent_time]).where(
        ModelUserHistory.user_hobby_id == user_hobby_id,
        ModelUserHistory.user_id == user_id,
        ModelUserHistory.date == date).order_by(sa.desc('actual_time')).limit(1)
    return await db.fetch_val(stm)


async def get_state_reflection_hobby(user_id: UUID4, user_hobby_id: int, date: datetime.date):
    urh = ModelUserReflectionHistory.t
    stm = sa.select([urh.c.level,
                     urh.c.is_correlation,
                     urh.c.correllation]).where(
        ModelUserHistory.user_hobby_id == user_hobby_id,
        ModelUserHistory.user_id == user_id,
        ModelUserHistory.date == date)

    return await db.fetch_one(stm)
