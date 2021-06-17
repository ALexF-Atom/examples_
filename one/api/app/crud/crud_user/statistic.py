import datetime
from pydantic import UUID4
import sqlalchemy as sa
from sqlalchemy.sql.expression import select
import sqlalchemy.dialects.postgresql as pg


from app.models.user import (ModelUserHistory, ModelUserReflectionDay,
                             ModelUserReflectionHistory, ModelUserHobby, ModelUserSettings)
from app.models.hobby import ModelHobby
from app.models.base import db


async def get_hobby(user_hobby_id: int, start: datetime.date, end: datetime.date):
    stm = sa.select([ModelUserHistory.date, ModelUserHistory.spent_time, ModelUserHistory.desired_time
                     ]).where(ModelUserHistory.user_hobby_id == user_hobby_id,
                              ModelUserHistory.date >= start,
                              ModelUserHistory.date <= end)\
        .order_by(ModelUserHistory.date)
    return await db.fetch_all(stm)


async def get_hobies(user_id: UUID4, start: datetime.date, end: datetime.date):
    h, hu, uh, us = ModelHobby.t, ModelUserHobby.t, ModelUserHistory.t, ModelUserSettings.t

    stm = (select([h.c.id.label('hobby_id'), h.c.title,
                  hu.c.id.label('user_hobby_id'), hu.c.name,
                  us.c.long,
                  uh.c.date, uh.c.spent_time, uh.c.planned_time,
                  uh.c.desired_time, uh.c.actual_time])
           .select_from(hu.join(h)
                        .join(us)
                        .join(uh, sa.and_(hu.c.id == uh.c.user_hobby_id,
                                          uh.c.date >= start, uh.c.date <= end), isouter=True))
           .where(hu.c.user_id == user_id)
           .order_by('user_hobby_id', 'date'))

    return await db.fetch_all(stm)


async def get_reflection(user_id: UUID4, start: datetime.date, end: datetime.date):
    # sa.literal_column('date')
    rd, rh = ModelUserReflectionDay.t, ModelUserReflectionHistory.t

    q_day = select([sa.cast(rd.c.id, sa.Boolean).label('day'), rd.c.date, rd.c.user_id]).where(
        rd.c.user_id == user_id, rd.c.date >= start, rd.c.date <= end).subquery()

    q_hobby = select([sa.func.array_agg(rh.c.user_hobby_id, type_=sa.Integer).label('user_hobies'),
                      rh.c.date,
                      rh.c.user_id]).where(rh.c.user_id == user_id,
                                           rh.c.date >= start,
                                           rh.c.date <= end).group_by('date', 'user_id').subquery()

    stm = select([q_day, q_hobby]).select_from(
        q_hobby.join(q_day, q_day.c.date == q_hobby.c.date, full=True)
    ).subquery()

    stm = select([sa.sql.label('date',
                               sa.case(
                                   [(stm.c.date != None, stm.c.date)],
                                   else_=stm.c.date_1)),
                  sa.cast(sa.case(
                      [(stm.c.user_hobies == None, [])],
                      else_=stm.c.user_hobies).label('user_hobies'), pg.ARRAY(sa.INTEGER)),
                  sa.cast(sa.case(
                      [(stm.c.day == True, '1')],
                      else_='0').label('day'),
        sa.Integer)]).order_by('date')

    return await db.fetch_all(stm)


async def get_reflection_v2(user_id: UUID4, start: datetime.date, end: datetime.date):
    rd, rh = ModelUserReflectionDay.t, ModelUserReflectionHistory.t

    h, hu = ModelHobby.t, ModelUserHobby.t

    q_day = select([sa.cast(rd.c.id, sa.Boolean).label('day'), rd.c.date, rd.c.user_id, rd.c.answers]).where(
        rd.c.user_id == user_id, rd.c.date >= start, rd.c.date <= end).subquery()

    q_hobby = select([rh.c.user_hobby_id,
                      rh.c.date,
                      rh.c.user_id,
                      rh.c.level,
                      rh.c.is_correlation,
                      rh.c.correllation]).where(rh.c.user_id == user_id,
                                                  rh.c.date >= start,
                                                  rh.c.date <= end).subquery()
    # return await db.fetch_all(q_hobby)

    stm = select([q_day, q_hobby]).select_from(
        q_hobby.join(q_day, q_day.c.date == q_hobby.c.date, full=True)
    ).subquery()

    stm = select([
        sa.sql.label('date',
                     sa.case(
                         [(stm.c.date != None, stm.c.date)],
                         else_=stm.c.date_1)),
        sa.cast(sa.case(
            [(stm.c.day == True, '1')],
            else_='0').label('day'), sa.Integer),
        sa.cast(sa.case(
            [(stm.c.answers != None, stm.c.answers)],
            else_=[]
        ).label('answers'), pg.ARRAY(pg.JSON)),
        stm.c.user_hobby_id,
        stm.c.level,
        stm.c.is_correlation,
        stm.c.correllation
    ]
    ).order_by('date').subquery()

    user_hobby = select([h.c.title, hu.c.id, hu.c.name]).select_from(
        hu.join(h)
    ).subquery()

    stm = select([stm, user_hobby.c.title, user_hobby.c.name]).where(
        user_hobby.c.id == stm.c.user_hobby_id)

    return await db.fetch_all(stm)
