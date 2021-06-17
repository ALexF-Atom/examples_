from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from pydantic.typing import NoneType

from app.utils.const_message import invalid_admin

API_KEY_NAME = "secret_uid"

admin_api_key = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

ADMIN_KEY = "secret"


async def auth_check_admin(admin_key: str = Security(admin_api_key)) -> NoneType:
    if admin_key != ADMIN_KEY:
        raise HTTPException(**invalid_admin)
