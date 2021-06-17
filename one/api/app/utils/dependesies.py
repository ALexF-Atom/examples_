from typing import Dict, Tuple, Union
import re
from databases.backends.postgres import Record
from fastapi import Request, HTTPException
from fastapi.logger import logger
from fastapi.security import OAuth2PasswordBearer

from app.schemas.schema_user import SchemaUserCreate
from app.crud import crud_user
from app.utils.const_message import invalid_user

from app.fsm.action_keys import ACTION_KEYS

schema_oauth = OAuth2PasswordBearer(tokenUrl='secret_token')


def get_params(request: Request) -> Dict[str, str]:
    return request.query_params


def user_params(request: Request) -> SchemaUserCreate:
    return SchemaUserCreate(**request.query_params)


async def is_user(user: SchemaUserCreate) -> Union[Record, HTTPException]:
    user = await crud_user.get(user.uid)
    if user is None:
        return HTTPException(**invalid_user)
    return user


async def get_actions_key(request: Request) -> Tuple[int, bool, int, int, bool]:
    rel_name_dict = request.path_params.copy()
    path = request.url.path
    method = request.method
    tz_info = int(request.headers.get('user_tz', 3))
    user_hobby_id = int(rel_name_dict.get('user_hobby_id', 0))
    
    for item in ACTION_KEYS:
        if re.match(item['path'], path) and item['method'] == method:
            return {'action_key': item.get('action_key', 0),
                    'tz_info': tz_info,
                    'rel_name_dict': rel_name_dict,
                    'user_hobby_id': user_hobby_id
                    }

