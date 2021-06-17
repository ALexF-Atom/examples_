from sqlalchemy import func
import sqlalchemy as sa
from app.models.base import Base


class ModelStories(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(64))

    date_created = sa.Column(sa.DateTime(timezone=True),
                             server_default=sa.text('now()'))

    active = sa.Column(sa.Boolean)
    priority = sa.Column(sa.SmallInteger, server_default='10')
    duration = sa.Column(sa.SmallInteger, server_default='15',
                         comment="Duration story in seconds")

    ...


class ModelStoryContent(Base):

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    ...

