import sqlalchemy as sa

from app.models.base import db
from app.models import ModelHelper, Button, Background


async def get(name: str):
  return await db.fetch_one(ModelHelper.t.select(ModelHelper.name == name))

async def get_id_for_mane(name: str):
  stm = sa.select([ModelHelper.id]).where(ModelHelper.name == name)
  return await db.fetch_val(stm)



async def get_id(id: int):
  hlp, btn, bg = ModelHelper.t, Button.t, Background.t
  stm = (sa.select([hlp,
                    btn,
                  #   btn.c.id.label('button_id'),
                    bg.c.colors.label('button_colors'),
                    bg.c.vector.label('button_vector')])
          .select_from(hlp.outerjoin(btn,
                                    btn.c.id == hlp.c.button_id)
                      .outerjoin(bg,
                                  btn.c.button_background_id == bg.c.id))
          .where(hlp.c.id == id))
  return await db.fetch_one(stm)
