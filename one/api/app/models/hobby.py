import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from app.models.base import Base


class ModelHobby(Base):
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    title = sa.Column(sa.String(32), nullable=False)
    description = sa.Column(sa.Text, nullable=True)
    icon_id = sa.Column(sa.ForeignKey('icon.id', ondelete='CASCADE'))
    is_enabled = sa.Column(sa.Boolean, server_default='1')


class What(Base):
    ...



class Where(Base):
    ...



class Long(Base):
    ...


