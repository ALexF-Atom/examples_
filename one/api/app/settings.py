import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_URL = '/templates/'
TEMPLATES_ROOT = f'{BASE_DIR}{TEMPLATES_URL}'

DB_USER = os.environ.get("DB_USERNAME")
DB_PASS = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

DEBUG = bool(int(os.environ.get("DEBUG")))
ENV = os.environ.get("ENV")

APP_PORT = int(os.environ.get("APP_PORT"))
APP_HOST = os.environ.get("APP_HOST")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
