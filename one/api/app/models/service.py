import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from app.models.base import Base


class ModelTag(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    tag = sa.Column(sa.String(32))


class ScriptTags(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    tag_id = sa.Column(sa.ForeignKey(
        'model_tag.id', ondelete="CASCADE"))
    script_id = sa.Column(sa.ForeignKey(
        'model_script.id', ondelete='CASCADE'))


class AnswerTags(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    tag_id = sa.Column(sa.ForeignKey(
        'model_tag.id', ondelete="CASCADE"))
    answer_id = sa.Column(sa.ForeignKey(
        'model_answer.id', ondelete='CASCADE'))


class QuestTags(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    tag_id = sa.Column(sa.ForeignKey(
        'model_tag.id', ondelete="CASCADE"))
    quest_id = sa.Column(sa.ForeignKey(
        'model_quest.id', ondelete='CASCADE'))


class BackgroundTags(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    tag_id = sa.Column(sa.ForeignKey(
        'model_tag.id', ondelete="CASCADE"))
    background_id = sa.Column(sa.ForeignKey(
        'background.id', ondelete='CASCADE'))


class HelperTags(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    tag_id = sa.Column(sa.ForeignKey(
        'model_tag.id', ondelete="CASCADE"))
    helper_id = sa.Column(sa.ForeignKey(
        'model_helper.id', ondelete='CASCADE'))



class Background(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(32), nullable=True)
    colors = sa.Column(sa.String(64))
    vector = sa.Column(sa.SmallInteger)


class Button(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(32), nullable=True)
    ...


class Icon(Base):
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    title_icon = sa.Column(sa.String(32), nullable=False)
    img_icon = sa.Column(sa.Text, nullable=True)


class IconState(Base):
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    icon_id = sa.Column(sa.ForeignKey('icon.id', ondelete='CASCADE'))
    title_state = sa.Column(sa.String(32), nullable=False)
    color_id = sa.Column(sa.ForeignKey(
        'background.id', ondelete='SET NULL'), nullable=True)
    opacity = sa.Column(sa.Float, server_default='1.0')


class TimeInterval(Base):
    __table_args__ = (sa.UniqueConstraint('start', 'end', name='unique_time'),)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(32))
    start = sa.Column(sa.Time)
    end = sa.Column(sa.Time)


class GroupNameHobby(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(32))


class GroupHobby(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    group_id = sa.Column(sa.ForeignKey('group_name_hobby.id', ondelete='CASCADE'))
    hobby_id = sa.Column(sa.ForeignKey('model_hobby.id', ondelete='CASCADE'))


class Day(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    day = sa.Column(sa.SmallInteger)


class NameGroupDay(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String(32))


class GroupDay(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    named_group_day_id = sa.Column(sa.ForeignKey('name_group_day.id',
                                                 ondelete='CASCADE'))
    day_id = sa.Column(sa.ForeignKey('day.id', ondelete='CASCADE'))
