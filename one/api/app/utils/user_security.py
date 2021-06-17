from typing import Tuple, Dict
from databases.backends.postgres import Record
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from pydantic import UUID4
from asyncpg.exceptions import DataError

from app.crud import crud_user
from app.utils.const_message import invalid_user, invalid_user_hobby
from app.utils.dependesies import get_actions_key
from app.fsm.user_state_machine import UserStateMachine
from app.fsm import crud_fsm

USER_API_KEY = APIKeyHeader(name='secret_uid')


async def auth_check_get_user(user_id: UUID4 = Depends(USER_API_KEY),
                             event_data: Dict = Depends(get_actions_key)) -> UserStateMachine:
    try:
        if await crud_user.exists_user(user_id):
            #print(.*)
            if event_data['user_hobby_id']:
                if not await crud_user.hobby.auth_is_user_hobby_id(user_id, event_data['user_hobby_id']):
                    raise HTTPException(**invalid_user_hobby)
            #print(.*)
            user = UserStateMachine(user_id, **event_data)
            
            await user.start()
            #print(.*)
            yield user
            #print(.*)
            await user.stop()
            #print(.*)
            return
    except DataError as e:
        #print(.*)
        raise HTTPException(**invalid_user)
    #print(.*)
    raise HTTPException(**invalid_user)


async def auth_check_is_user(user_id: UUID4 = Depends(USER_API_KEY))->UUID4:
    try:
        if await crud_user.exists_user(user_id):
            return user_id
    except DataError as e:
        raise HTTPException(**invalid_user)
    raise HTTPException(**invalid_user)
