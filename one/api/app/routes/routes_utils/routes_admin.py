from fastapi import APIRouter, status, Depends, HTTPException, Request
from fastapi.logger import logger
from typing import List, Literal
from pydantic import UUID4
from app.fsm.user_state_machine import UserStateMachine
from sqlalchemy.sql.expression import bindparam

from app.schemas.schema_user import SchemaUser
from app.schemas.schema_message import SchemaMessageDelete

from app.utils.admin_security import auth_check_admin
from app.utils.utils import drop_and_create_db, upgrade_migrate_db
from app.utils.const_message import not_found

from app.models.base import db

import app.models.reflections as mrf
import app.models.script as msc
import app.models.helper as mhp
import app.models.stories as mstory
import app.models.levels as mlv
import app.models.hobby as mhb
import app.models.service as msrs
import app.models.event_key as ek

from app.crud import crud_hobby, crud_user

import test.json_reflection as jrf
import test.json_script as jsc
import test.json_helper as jhp
import test.json_story as jstory
import test.json_level as jlv
import test.json_tag as jtag
import test.json_data as jhb
import test.json_achievement as jachv
import test.json_evkey as evk



admin = APIRouter(prefix='/admin', tags=["""Admin routes"""],
                  dependencies=[Depends(auth_check_admin)])



@admin.get('/all', status_code=status.HTTP_200_OK,
           description="bb42cc51-4b4b-4da2-a5ad-01244ebc68d2",
           response_model=List[SchemaUser])
async def get_users():
    return await crud_user.alls()


@admin.delete('/delete-user/{uid}',
              response_model=SchemaMessageDelete,
              description='Delete User by admin',
              status_code=status.HTTP_200_OK)
async def delete_user(uid: str):
    if crud_user.exists_user(uid=uid):
        return {'uid': await crud_user.delete(uid)}
    raise HTTPException(**not_found)



@admin.get('/clear-db',
           status_code=status.HTTP_200_OK,
           description="Drop db and create by admmin")
async def clear_db():
    await db.disconnect()
    db_name = drop_and_create_db()
    await db.connect()
    return {'message': f'Drop database {db_name}'}


@admin.get('/alembic-migrate-db',
           status_code=status.HTTP_200_OK,
           description="Drop db and create by admmin")
async def alembic_migrate_db():
    await db.disconnect()
    upgrade_migrate_db()
    await db.connect()
    with open('versions.py', 'a') as f:
        f.write('version=1\n')
    return {'message': 'Alembic Upgrade head',
            'status': db.is_connected}


@admin.get('/data-filling-db',
           status_code=status.HTTP_200_OK,
           description="Filling the database with the necessary data")
async def data_filling_db(request: Request):
    models_message = [...]
    try:
        ...
    
    except Exception as e:
        logger.warning(e)
        message = (f'Not create: {",".join(models_message)}')
        
    else:
        message = 'successes'
 
    return {'message': message,
            'notes': 'Be sure to do the migration for the admin panel and create the necessary users'}
