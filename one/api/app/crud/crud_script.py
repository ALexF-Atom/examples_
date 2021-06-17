from sqlalchemy.sql.functions import array_agg
from app.models.base import db
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from typing import Dict, List, Tuple

from app.models import (ModelQuestAnswer, ModelScriptQuest,
                        ModelScript, ModelAnswer,
                        ModelQuest, Background)


async def get_script_(script_id: int):
    q, a, sq, s = ModelQuest.t, ModelAnswer.t, ModelScriptQuest.t, ModelScript.t
    stm = sa.select([sq.c.order, sq.c.quest_id, q.c.quest, a.c.answer_type, a.c.answer_data]).select_from(
        sq.join(q.join(a))
    ).where(sq.c.script_id == script_id)
    return await db.fetch_all(stm)


async def get_script(script_id: int):
    q, a, q, sq, s, qa = (ModelQuest.t, ModelAnswer.t, ModelQuest.t,
                          ModelScriptQuest.t, ModelScript.t, ModelQuestAnswer.t)
    bg = Background.t

    sub = (sa.select([sa.func.array_agg(
        sa.tuple_(a.c.answer, qa.c.text_color, bg.c.colors, bg.c.vector, qa.c.order),
        type_=sa.TEXT
    )
                      .label('answer_data'),
                      q.c.quest, q.c.id])
           .select_from(
        q.join(qa)
        .outerjoin(a, a.c.id == qa.c.answer_id)
        .outerjoin(bg, bg.c.id == qa.c.answer_background_id))
        .group_by(q.c.quest, q.c.id, )
        .subquery())

    stm = (sa.select([
        sub.c.quest,
        sub.c.answer_data,
        sub.c.id.label('quest_id'),
        sq,
        s.c.name.label('script_title')
         ])
        .select_from(
            sub.join(sq, sq.c.quest_id == sub.c.id)
            .outerjoin(s, s.c.id==sq.c.script_id)
            )
        .where(s.c.id == script_id).order_by(sq.c.order))
    return await db.fetch_all(stm)


async def get_quest_data(quest_id: int):
    q, a, qa, b = ModelQuest.t, ModelAnswer.t, ModelQuestAnswer.t, Background.t
    stm = sa.select([q.c.quest.label('quest_title'), q.c.answer_type,
                     qa.c.quest_id, b.c.colors, b.c.vector,
                     a.c.answer]).select_from(qa.join(a).join(q).outerjoin(b)).where(qa.c.quest_id == quest_id)
    return await db.fetch_all(stm)


async def all_quest_data(ids: Tuple[int]):
    q, a, qa, b = ModelQuest.t, ModelAnswer.t, ModelQuestAnswer.t, Background.t
    stm = sa.select([q.c.quest.label('quest_title'), q.c.answer_type,
                     qa.c.quest_id, b.c.colors, b.c.vector,
                     a.c.answer]).select_from(qa.join(a).join(q).outerjoin(b)).where(qa.c.quest_id == sa.any_(ids))
    return await db.fetch_all(stm)


async def get_background(bid: int):
    return await db.fetch_one(Background.t.select(Background.id == bid))
