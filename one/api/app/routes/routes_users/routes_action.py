
from app.schemas.schema_level import NotificationAchievement
from fastapi import HTTPException
from typing import List

from fastapi import status,  Depends

from app.fsm.user_state_machine import UserStateMachine
from app.utils.user_security import auth_check_get_user, auth_check_is_user
from pydantic import UUID4


from app.crud import crud_level
from app.schemas.schema_script import SchemaScript
from app.schemas.schema_user.history import SchemaAnswer
from app.schemas.schema_message import SchemaMessageCreate, NotificationCreate

from app.routes.routes_users import user


@user.get('/action/{button_id}',
        status_code=status.HTTP_200_OK,
        response_model=SchemaMessageCreate,
        description="""
        Сообщает о том, что кнопка нажата
        для действий вне контекста приложения
        """)
async def receive_signal_action(button_id: int,
                                user_id: UUID4 = Depends(auth_check_is_user)):
    return {}


@user.get('/close',
          status_code=status.HTTP_200_OK,
          description="""
          Сообщает о том, что приложение закрыто
          """)
async def signal_close_app(user_id: UUID4 = Depends(auth_check_is_user)):
    return {}


@user.get('/open-screen/{action_key}',
        status_code=status.HTTP_200_OK,
        description="""
        Сообщает о том, на какой экран пользователь перешел
        100: 'open_screen_home'
        102: "open_screen_analitics_hobby",
        104: "open_screen_analitics_reflection",
        106: 'open_screen_levels_and_events',
        108: 'open_screen_timer',
        110: 'open_screen_reflection_hobby',
        112: 'open_screen_reflection_day',

        320: 'open_screen_user_hobby',
        322: 'open_screen_all_hobby',
        324: 'open_screen_user_profile',
        114: 'open_screen_quiz',
          """)
async def action_open_screen(action_key: int,  user: UserStateMachine = Depends(auth_check_get_user)):
    return {'notification': user.app.event_key}



@user.get('/notification/{event_key}',
          response_model=NotificationAchievement,
          responses={404: {"description": "The item was not found"}},
          status_code=status.HTTP_200_OK,
          description="""
  Поздравлялка
            Ожидаемый параметр "event_key", который приходит в ключе "notification" в ответах сервера

            Приходит
                data
                achievement_id      - ид-ачивки
                navigation_title  - верхний заголовок
                achievement_image   - сслыка на картинку
                position_image      - позиция на экране ['top', 'bottom', 'center']
                achievement_title   - заголовок в формате html
                achievement_text    - текст в формате html
                share_image         - ссылка  на картинку для шаринга
                achievement_colors  - заливка
                achievement_vector  - направление заливки
                button_text         - текст кнопки в формате html
                button_url          - ссылка на ресурс
                button_id_script    - идишник скрипта
                position_button     - позиция кнопки
                button_colors       - заливка для фона кнопки
                button_vector       - направление заливки
                button_id           - ид-кнопки для отправки сигнала на сервер о ее нажатии
                                        '/user/action/{button_id}'
            """)
async def get_achievments(event_key: int,
                          user_id: UUID4 = Depends(auth_check_is_user)):
    if await UserStateMachine.compare_and_confirmation_event_completed(user_id=user_id,
                                                                       event_id=event_key):
        data = await crud_level.get_achievment(event_key=event_key)
        if data is not None:
            return {'data': data}

    raise HTTPException(status_code=404, detail="Item not found")
