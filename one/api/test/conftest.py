import pytest
import os
from alembic.config import Config
from alembic import command
import sqlalchemy_utils as su
from starlette.testclient import TestClient

# Устанавливаем `os.environ`, чтобы использовать тестовую БД
os.environ['TESTING'] = '1'

from main import app
from app.models import base
from app.settings import BASE_DIR


@pytest.fixture(scope="module")
def app_test():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="module")
def db_test():
    if not su.database_exists(base.DATABASE_URI):
        su.create_database(base.DATABASE_URI)
    alembic_cfg = Config(os.path.join(BASE_DIR, "alembic.ini"))
    command.upgrade(alembic_cfg, "head")
    try:
        yield base.DATABASE_URI
    finally:
        su.drop_database(base.DATABASE_URI)

