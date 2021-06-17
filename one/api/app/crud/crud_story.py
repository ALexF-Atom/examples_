
from typing import Dict
import sqlalchemy as sa
from app.models.base import db
from pydantic import UUID4

from app.models import (ModelStories, Button,
                        ModelUserStory, Background,
                        ModelScript, ModelQuest,
                        ModelStoryContent)
from app.models.user import ModelUserStory


async def save(data: Dict):
    stm = ModelUserStory.t.insert()
    return await db.execute(query=stm, values=data)


async def is_view(user_id: UUID4, story_id: int):
    return await db.fetch_val(sa.select(sa.exists().where(sa.and_(ModelUserStory.user_id == user_id,
                                                                  ModelUserStory.story_id == story_id))))


async def update(user_id: UUID4, story_id: int, data: Dict):
    stm = (ModelUserStory.t.update()
           .where(sa.and_(ModelUserStory.user_id == user_id, ModelUserStory.story_id == story_id))
           .values(**data)
           .returning(ModelUserStory.story_id))
    return await db.execute(stm)


async def get(user_id: UUID4):
    prbg = Background.t.alias()
    s, us = ModelStories.t, ModelUserStory.t
    stm = sa.select([
        s,
        prbg.c.colors.label('preview_colors'),
        prbg.c.vector.label('preview_vector'),
        sa.cast(
            sa.case(
                [(us.c.user_id == None, '1')],
                else_='0').label('is_active'),
            sa.Boolean
        ),
        us.c.like_is,
    ]).select_from(
        s.join(us, sa.and_(s.c.id == us.c.story_id,
               us.c.user_id == user_id), isouter=True)
        .join(prbg, s.c.preview_background_id == prbg.c.id, isouter=True)
    ).order_by(sa.desc('is_active'), sa.desc(s.c.priority), sa.desc(s.c.date_created))
    return await db.fetch_all(stm)


async def get_content(story_id: int):
    cbg = Background.t.alias()
    btnbg = Background.t.alias()
    sc, btn, scr = ModelStoryContent.t, Button.t, ModelScript.t

    stm = sa.select([sc,
                     btn,
                     cbg.c.colors.label('content_background'),
                     cbg.c.vector.label('content_vector'),
                     btnbg.c.colors.label('button_background'),
                     btnbg.c.vector.label('button_vector'),
                     scr,
                     ]).select_from(
        sc.outerjoin(btn, sc.c.button_id == btn.c.id)
        .outerjoin(cbg, sc.c.content_background_id == cbg.c.id)
        .outerjoin(btnbg, btn.c.button_background_id == btnbg.c.id)
        .outerjoin(scr, sc.c.script_id == scr.c.id)).where(
            sc.c.story_id == story_id).order_by(sa.asc(sc.c.order))

    return await db.fetch_all(stm)


async def bulk_save(data):
    stm = ModelStories.t.insert()
    return await db.execute_many(query=stm, values=data)


async def get_is_like(user_id: UUID4, story_id: int):
    stm = sa.select([ModelUserStory.like_is]).where(ModelUserStory.user_id == user_id,
                                                    ModelUserStory.story_id == story_id)
    return await db.fetch_val(stm)

