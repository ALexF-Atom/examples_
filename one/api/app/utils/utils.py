import jwt
from typing import Dict
from alembic.config import Config
from alembic import command
import sqlalchemy_utils as su
import os

from app.settings import SECRET_KEY, ALGORITHM, BASE_DIR
from app.models.base import DATABASE_URI

access_email = ["admin@praqtiqa.com"]


def create_token(*, data: Dict[str, str]) -> str:
    secret_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return secret_token


def decode_token(*, secret_token: str) -> Dict[str, str]:
    data = jwt.decode(secret_token, SECRET_KEY, algorithms=ALGORITHM)
    return data


def validate_admin(data: Dict[str, str]) -> bool:
    return data['email'] in access_email


def drop_and_create_db():
    su.drop_database(DATABASE_URI)
    su.create_database(DATABASE_URI)
    return DATABASE_URI


def upgrade_migrate_db():
    alembic_cfg = Config(os.path.join(BASE_DIR, "alembic.ini"))
    command.upgrade(alembic_cfg, "head")


