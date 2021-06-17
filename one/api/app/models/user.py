import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.sql.expression import false
import sqlalchemy as sa

from app.models.base import Base


class ModelUser(Base):
    uid = sa.Column(pg.UUID(), primary_key=True)
    is_registered = sa.Column(sa.Boolean, server_default=false())
    created_at = sa.Column(sa.DateTime(timezone=True),
                           server_default=sa.text('now()'))


class ModelUserHobby(Base):
    __table_args__ = (sa.UniqueConstraint(
        'user_id', 'hobby_id', 'name', name='unique_hobby'),)

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    user_id = sa.Column(sa.ForeignKey('model_user.uid',
                                      ondelete='CASCADE'), nullable=False)
    hobby_id = sa.Column(sa.ForeignKey('model_hobby.id',
                                       ondelete='CASCADE'), nullable=False)
    started_at = sa.Column(sa.DateTime(timezone=True),
                           server_default=sa.text('now()'))
    completed_at = sa.Column(sa.DateTime(timezone=True), nullable=True)
    name = sa.Column(sa.String(32), server_default='My hobby')


class ModelUserSettings(Base):
    __table_args__ = (sa.UniqueConstraint(
        'user_id', 'user_hobby_id', name='unique_hobby_settings'),)
    ...


class ModelUserAlarm(Base):
    __table_args__ = (sa.UniqueConstraint(
        'user_id', 'user_hobby_id', name='unique_hobby_alarm'),)
    ...


class ModelUserHistory(Base):
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    user_hobby_id = sa.Column(sa.ForeignKey('model_user_hobby.id',
                                            ondelete='CASCADE'),
                              nullable=False)
    ...


class ModelUserReflectionHistory(Base):
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    user_hobby_id = sa.Column(sa.ForeignKey('model_user_hobby.id',
                                            ondelete='CASCADE'),
                              nullable=False, index=True)
    ...


class ModelUserReflectionDay(Base):
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    user_id = sa.Column(sa.ForeignKey('model_user.uid',
                                      ondelete='CASCADE'),
                        nullable=False, index=True)
    ...


class ModelUserStory(Base):
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    ...


class ModelUserLevel(Base):
    __table_args__ = (sa.UniqueConstraint(
        'user_id', 'level_id', 'user_hobby_id', name='unq_level'),)
    ...
class ModelUserEvent(Base):
    __table_args__ = (sa.UniqueConstraint(
        'user_id', 'event_id', 'user_hobby_id', name='unq_event'),)
    ...
