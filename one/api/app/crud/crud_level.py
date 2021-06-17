import sqlalchemy as sa
from sqlalchemy.sql.expression import text
from app.models.base import db
from pydantic import UUID4
import datetime

from app.models import (Background, ModelUserLevel,
                        ModelUserEvent, ModelEvent,
                        ModelLevel, Achievement, Button,
                        ModelEventKey)


async def current_user_level(user_id: UUID4, current_level: int):
    l, bg = ModelLevel.t, Background.t
    stm = (sa.select([l.c.level_title,
                      l.c.level_image,
                      bg.c.colors.label('level_colors'),
                      bg.c.vector.label('level_vector')
                      ])
           .select_from(l.outerjoin(bg, bg.c.id == l.c.level_background_id))
           ).where(l.c.level_stage==current_level)
    return await db.fetch_one(stm)


async def get_user_level(user_id: UUID4, user_hobby_id: int):
    lbg = Background.t.alias()
    ebg = Background.t.alias()
    l, e, ue = ModelLevel.t, ModelEvent.t, ModelUserEvent.t

    stm = sa.select([
        l.c.level_enabled,
        l.c.level_title,
        l.c.level_name,
        l.c.level_description,
        l.c.level_image,
        l.c.level_stage,
        l.c.level_background_id,
        l.c.level_helper_id,
        e.c.event_name,
        e.c.event_title,
        e.c.event_description,
        e.c.event_image,
        e.c.event_stage,
        e.c.event_background_id,
        e.c.event_helper_id,
        lbg.c.colors.label('level_colors'),
        lbg.c.vector.label('level_vector'),
        ebg.c.colors.label('event_colors'),
        ebg.c.vector.label('event_vector'),
        ue.c.user_id.label('is_completed'),

        # (sa.case(
        #     [(ue.c.user_id == None, '0')],
        #         else_='1')).label('is_completed'),

    ]).select_from(
        e.join(l)
        .join(ebg, e.c.event_background_id == ebg.c.id, isouter=True)
        .outerjoin(lbg, l.c.level_background_id == lbg.c.id)
        .join(ue, sa.and_(e.c.id == ue.c.event_id,
                          ue.c.user_id == user_id,
                          ue.c.user_hobby_id == user_hobby_id), isouter=True)
    )
    return await db.fetch_all(stm)


async def get_achievment(event_key: int):
    abg = Background.t.alias()
    btnbg = Background.t.alias()
    a, btn, ev = Achievement.t, Button.t, ModelEventKey.t
    stm = sa.select([
        a.c.id.label('achievement_id'),
        a.c.navigation_title,
        a.c.achievement_image,
        a.c.position_image,
        a.c.achievement_text,
        a.c.achievement_title,
        a.c.position_button,
        a.c.share_image,
        abg.c.colors.label('achievement_colors'),
        abg.c.vector.label('achievement_vector'),
        a.c.achievement_button_id.label('button_id'),
        btn.c.button_text,
        btn.c.button_url,
        btn.c.button_id_script,
        btnbg.c.colors.label('button_colors'),
        btnbg.c.vector.label('button_vector'),
    ]).select_from(
        a.outerjoin(btn, a.c.achievement_button_id == btn.c.id)
        .outerjoin(abg, a.c.achievement_background_id == abg.c.id)
        .outerjoin(btnbg, btn.c.button_background_id == btnbg.c.id)
        .outerjoin(ev, ev.c.achievement_id == a.c.id)
    ).where(ev.c.event_id == event_key)
    return await db.fetch_one(stm)


async def get_current_level_event(user_id: UUID4, level_stage: int):
    event, level, user = ModelEvent.t, ModelLevel.t, ModelUserEvent.t
    stm = sa.select([event.c.id.label('event_id'),
                     event.c.event_stage.label('stage'),
                     ]).select_from(
        event.join(level)
    ).where(level.c.level_stage == level_stage).where(
        ~sa.exists().where(
            sa.and_(user.c.event_id == event.c.id,
                    user.c.user_id == user_id))
    ).order_by('event_stage')
    return await db.fetch_all(stm)


async def get_level_event_id(level_stage: int):
    stm = sa.select([ModelLevel.id]).where(
        ModelLevel.level_stage == level_stage)
    return await db.fetch_val(stm)


