import sqlalchemy as sa
from app.models.base import Base


class ModelLevel(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    level_enabled = sa.Column(sa.Boolean, server_default='1')
    level_name = sa.Column(sa.String(32))
    level_title = sa.Column(sa.String(64))
    level_description = sa.Column(sa.Text)
    level_image = sa.Column(sa.Text)
    level_stage = sa.Column(sa.SmallInteger, autoincrement=True)
    
    ...


class ModelEvent(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    event_title = sa.Column(sa.String(64))
    event_name = sa.Column(sa.String(32))
    event_description = sa.Column(sa.Text)
    event_image = sa.Column(sa.Text)
    event_stage = sa.Column(sa.SmallInteger, autoincrement=True)
    event_level_id = sa.Column(sa.ForeignKey(
        'model_level.id', ondelete='SET NULL'), nullable=True)
    
    ...

class Achievement(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    ...