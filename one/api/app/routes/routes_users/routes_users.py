from fastapi import status, Depends
from pydantic import UUID4
from app.fsm.user_state_machine import UserStateMachine

from app.utils.user_security import auth_check_get_user, auth_check_is_user
from app.fsm import crud_fsm
from app.crud import crud_user
from app.schemas.schema_user import SchemaUserCreate, NotificationUserHobby
from app.schemas.schema_message import NotificationDelete

from app.routes.routes_users import user


@user.post('/create',
           response_model=SchemaUserCreate,
           status_code=status.HTTP_201_CREATED, description='Create User')
async def create_user():
    user_id = await crud_user.create()
    return {'uid': user_id}


@user.get('/hobby',
          response_model=NotificationUserHobby,
          status_code=status.HTTP_200_OK,
          description="""
          Returns all user habits
    data - данные для работы: >>
        * id глобальный     Идентификатор привычки
        * title             Глобальное название привычки
        * description       Описание глобальной привычки
        * user_hobby_id     Идентификатор пользовательской привычки
        * user_hobby_name   Дополнительный идентификатор пользовательской привычки,
                            обеспечивающий возможность создания разных пользовательских привычек одной глобальной привычки,
                            создается по умолчанию, если явно не передан.
    
    
        """)
async def get_user_hobby_all(user_id: UUID4 = Depends(auth_check_is_user)):
    
    return {'data': await crud_user.hobby.get(user_id),}


@user.delete('/hobby/{user_hobby_id}',
             response_model=NotificationDelete,
             status_code=status.HTTP_200_OK,
             description='Removing a user hobby')
async def delete_user_hobby(user_hobby_id: int,
                            user_id: UUID4 = Depends(auth_check_is_user)):
    await crud_user.hobby.delete(user_hobby_id=user_hobby_id,
                                 user_id=user_id)
    return {'data': {'id': user_hobby_id},
           }



@user.delete('/delete',
             response_model=NotificationDelete,
             status_code=status.HTTP_200_OK,
             description='Removing user')
async def delete_user(user_id: UUID4 = Depends(auth_check_is_user)):
    await crud_user.delete(user_id=user_id)
    return {'data': {'id': user_id},
           }

