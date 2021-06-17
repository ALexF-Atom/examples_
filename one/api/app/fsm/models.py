import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from app.models.base import Base


class ModelFSM(Base):
    user_id = sa.Column(pg.UUID, primary_key=True)
    current_hobby_id = sa.Column(sa.SmallInteger,
                                      server_default=sa.text('0'))
    count_user_hobby = sa.Column(sa.SmallInteger,
                                 server_default=sa.text('0'))
    start_day = sa.Column(sa.Date,
                          server_default=sa.text('now()'))
    current_day = sa.Column(sa.Date,
                            nullable=True)
    last_day = sa.Column(sa.Date,
                         nullable=True)
    last_day_doing_reflection_day = sa.Column(sa.Date,
                                              nullable=True)
    current_level = sa.Column(sa.SmallInteger,
                              server_default=sa.text('1'))
    progress_level = sa.Column(sa.SmallInteger,
                               server_default=sa.text('0'))
    in_a_row_day_open_app = sa.Column(sa.SmallInteger,
                                      server_default=sa.text('0'))
    max_row_day_open_app = sa.Column(sa.SmallInteger,
                                     server_default=sa.text('0'))
    in_a_row_day_doing_reflection_day = sa.Column(sa.SmallInteger,
                                                  server_default=sa.text('0'))
    no_active_in_a_row_day = sa.Column(sa.SmallInteger,
                                       server_default=sa.text('0'))
    no_active_in_a_row_day_reflection_day = sa.Column(sa.SmallInteger,
                                                      server_default=sa.text('0'))
    next_day_is_day_off = sa.Column(sa.Date, nullable=True)
    event_key = sa.Column(sa.SmallInteger,
                          server_default=sa.text('0'))


class ModelFSM_Hobby(Base):
    __table_args__ = (sa.UniqueConstraint(
        'user_id', 'user_hobby_id', name='unique_user_hobby'),)
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    user_id = sa.Column(pg.UUID)
    user_hobby_id = sa.Column(sa.Integer)
    hobby_last_day = sa.Column(sa.Date,
                               server_default=sa.text('now()'))
    last_day_doing_routine = sa.Column(sa.Date,
                                       nullable=True)
    last_day_doing_reflection_routine = sa.Column(sa.Date,
                                                  nullable=True)
    in_a_row_day_doing_routine = sa.Column(sa.SmallInteger,
                                           server_default=sa.text('0'))
    in_a_row_day_doing_reflection_routine = sa.Column(sa.SmallInteger,
                                                      server_default=sa.text('0'))
    no_active_in_a_row_day_doing_routine = sa.Column(sa.SmallInteger,
                                           server_default=sa.text('0'))
    no_active_in_a_row_day_doing_reflection_routine = sa.Column(sa.SmallInteger,
                                                      server_default=sa.text('0'))


class ModelUserRelationAction(Base):

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.ForeignKey('model_user.uid',
                                      ondelete='CASCADE'), index=True)
    action_key = sa.Column(sa.SmallInteger, index=True)
    related_name = sa.Column(sa.String(32))
    key_id = sa.Column(sa.Integer,  nullable=True, index=True)
    created_at = sa.Column(sa.DateTime, server_default=sa.text('now()'))


class UserNoConfirmEvent(Base):
    __table_args__ = (sa.UniqueConstraint(
        'user_id', 'event_id', name='unique_lost_event'),)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(pg.UUID, index=True)
    event_id = sa.Column(sa.Integer, index=True)
