import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from app.models.base import Base


class ModelEventKey(Base):
    id = sa.Column(sa.Integer,  primary_key=True, autoincrement=True)
    ...


class RulesEvent(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    event_key_id = sa.Column(sa.ForeignKey('model_event_key.id',
                                           ondelete='CASCADE'))
    ...


class RulesLevel(Base):
    ...


class RulesStory(Base):
   ...

class RulesScript(Base):

    ...


class ActionUserSettings(Base):
    ...


class UserAction(Base):
   
   ...


class ModelAction(Base):
    ...

class RulesContent(Base):
   ...


class RulesQuest(Base):
   ...

class RulesButton(Base):
   ...


class RulesHelper(Base):
    ...
