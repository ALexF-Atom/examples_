from fastapi import status, HTTPException, Depends
from fastapi.logger import logger
from pydantic import UUID4
from app.fsm.user_state_machine import UserStateMachine

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError

import app.schemas.schema_user as sch
from app.schemas.schema_message import NotificationUpdate
from app.utils.user_security import auth_check_get_user, auth_check_is_user
from app.crud import crud_user

from app.routes.routes_users import user
from app.fsm import crud_fsm


@user.get('/properties/{user_hobby_id}',
          response_model=sch.NotificationUserHobbySettingsResponse,
          status_code=status.HTTP_200_OK,
          description="""Get the properties of a user's habit""")
async def get_hobby_properties(user_hobby_id: int, user_id: UUID4 = Depends(auth_check_is_user)):
    data = await crud_user.properties.get(user_id=user_id, user_hobby_id=user_hobby_id)
    if data is not None:
        return {'data': data}
    raise HTTPException(status_code=404, detail="Item not found")


@user.post('/properties',
           response_model=sch.NotificationUserHobbySettingsModel,
           status_code=status.HTTP_201_CREATED,
           description="Preserving the properties of a user's habit")
async def create_hobby_with_properties(hobby: sch.SchemaUserHobbyPost,
                                       user_id: UUID4 = Depends(auth_check_is_user)):
    try:
        user_hobby_id = await crud_user.hobby.save(user_id=user_id,
                                                   hobby_id=hobby.hobby_id)
    except ForeignKeyViolationError:
        raise HTTPException(status_code=404, detail="Hobby Item not found")
    except UniqueViolationError:
        user_hobby_id = await crud_user.hobby.get_user_hobby_id(user_id=user_id,
                                                                hobby_id=hobby.hobby_id)

    user_hobby = sch.SchemaUserHobbySettingsModel(user_hobby_id=user_hobby_id,
                                                  **dict(hobby))

    try:
        await crud_user.properties.save(user_id=user_id,
                                        user_hobby=dict(user_hobby))
    except ForeignKeyViolationError:
        raise HTTPException(status_code=404, detail="Hobby Item not found")
    except UniqueViolationError:
        await crud_user.properties.update(user_id=user_id,
                                          user_hobby_id=user_hobby_id,
                                          properties_update=dict(user_hobby))

    try:
        data = dict(sch.SchemaUserAlarmModel(user_hobby_id=user_hobby_id,
                                             time='9:00',
                                             notification=False))
        await crud_user.alarm.save(user_id=user_id, data=data)
    except ForeignKeyViolationError:
        raise HTTPException(status_code=404, detail="Hobby Item not found")
    except UniqueViolationError:
        data = dict(sch.SchemaUserAlarm(time='9:00',
                                        notification=False))
        await crud_user.alarm.update(user_id=user_id,
                                     user_hobby_id=user_hobby_id,
                                     settings_update=data)
                                     
    await UserStateMachine.init(user_id=user_id, user_hobby_id=user_hobby_id)

    return {'data': {'user_hobby_id': user_hobby_id, **dict(hobby)},}


@user.get('/alarm/{user_hobby_id}',
          response_model=sch.NotificationUserAlarm,
          status_code=status.HTTP_200_OK,
          description="Get setting time")
async def get_hobby_alarm(user_hobby_id: int, user_id: UUID4 = Depends(auth_check_is_user)):
    data = await crud_user.alarm.get(user_id=user_id, user_hobby_id=user_hobby_id)
    if data is not None:
        return {'data': data,
               
                }
    raise HTTPException(status_code=404, detail="Item not found")


@user.patch('/alarm/{user_hobby_id}',
            response_model=NotificationUpdate,
            status_code=status.HTTP_200_OK,
            description="Update settings time")
async def update_hobby_alarm(user_hobby_id: int, settings: sch.SchemaUserAlarm,
                             user_id: UUID4 = Depends(auth_check_is_user)):
    settings_update = settings.dict(exclude_unset=True)
    # logger.warning(f'request {settings_update}')

    data = await crud_user.alarm.update(user_id=user_id,
                                        user_hobby_id=user_hobby_id,
                                        settings_update=settings_update)
    return {'data': {'id': data},
           }


@user.patch('/properties/{user_hobby_id}',
            response_model=NotificationUpdate,
            status_code=status.HTTP_200_OK,
            description="Update the properties of a user's habit")
async def update_hobby_properties(user_hobby_id: int,
                                  properties: sch.SchemaUserHobbySettings,
                                  user_id: UUID4 = Depends(auth_check_is_user)):
    properties_update = properties.dict(exclude_unset=True)
    data = await crud_user.properties.update(user_id=user_id,
                                             user_hobby_id=user_hobby_id,
                                             properties_update=properties_update)
    if data is not None:
        return {'data': {'id': data},
               }
    raise HTTPException(status_code=404, detail="Item not found")
