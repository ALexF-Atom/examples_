from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from databases import Database
import sqlalchemy_utils as su
from sqlalchemy import MetaData

import os
import re

from sqlalchemy.sql.expression import Select

if os.environ.get('ENV') == 'development':
    from app.settings import DB_PORT, DB_USER, DB_PASS, DB_NAME, DB_HOST
else:
    from app.local_settings import DB_PORT, DB_USER, DB_PASS, DB_NAME, DB_HOST

if bool(int(os.environ['TESTING'])):
    DB_NAME = "async-test-app"

DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

db = Database(DATABASE_URI)

meta = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})


@as_declarative(metadata=meta)
class Base:
    @declared_attr
    def __tablename__(cls):
        pattern = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')
        return pattern.sub(r'_\1', cls.__name__).lower()

    @hybrid_property
    def t(self) -> Select:
        return self.__table__


metadata = Base.metadata

