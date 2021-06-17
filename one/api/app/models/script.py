import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from app.models.base import Base


class ModelScript(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.Text, comment='Name script', unique=True)
    # script_event_key_id = sa.Column(sa.ForeignKey('model_event_key.id',
    #                                        ondelete='SET NULL'))


class ModelAnswer(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    answer = sa.Column(sa.String(128), unique=True)


class ModelQuest(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    quest = sa.Column(sa.Text, unique=True)
    

class ModelScriptQuest(Base):
    order = sa.Column(sa.SmallInteger)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    ...
    



class ModelQuestAnswer(Base):
    order = sa.Column(sa.SmallInteger)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    ...
    



