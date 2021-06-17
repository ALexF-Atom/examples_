import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from app.models.base import Base


class ModelReflections(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    ...


class ModelReflectionsFinal(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    ...


class ModelReflectionsLevel(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    ...


class ModelLevelScript(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    ...


class ModelComplexity(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    ...
