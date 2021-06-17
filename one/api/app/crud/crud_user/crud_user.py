from typing import Iterable, NoReturn
from pydantic import UUID4
from databases.backends.postgres import Record
import uuid

from sqlalchemy.sql.expression import exists
from sqlalchemy import select

from app.models import ModelUser
from app.models.base import db


async def alls() -> Iterable[Record]:
    return await db.fetch_all(ModelUser.t.select())


async def create() -> UUID4:
    return await db.execute(ModelUser.t.insert().values(uid=uuid.uuid4()).returning(ModelUser.uid))


async def create_with_uid(uid: UUID4):
    return await db.execute(ModelUser.t.insert().values(uid=uid).returning(ModelUser.uid))


async def get(user_id: UUID4) -> Record:
    stm = ModelUser.t.select(ModelUser.uid == user_id)
    return await db.fetch_one(stm)


async def exists_user(user_id: UUID4) -> bool:
    return await db.execute(select(exists().where(ModelUser.uid == user_id)))


async def delete(user_id: UUID4) -> NoReturn:
    return await db.execute(ModelUser.t.delete(ModelUser.uid == user_id).returning(ModelUser.uid))


async def delete_all() -> NoReturn:
    return await db.execute(ModelUser.t.delete())
