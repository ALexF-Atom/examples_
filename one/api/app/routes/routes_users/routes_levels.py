from fastapi import status, Depends, HTTPException
from pydantic import UUID4
from app.fsm.user_state_machine import UserStateMachine
from itertools import groupby

from starlette.status import HTTP_204_NO_CONTENT

from app.utils.user_security import auth_check_get_user, auth_check_is_user

from app.crud import crud_level
from app.schemas.schema_level import NotificationLevel, NotificationAchievement

from app.routes.routes_users import user


@user.get('/level/{user_hobby_id}',
          response_model=NotificationLevel,
          status_code=status.HTTP_200_OK,
          description="""
        Ожидает
            user_hobby_id               - ид-шник пользовательского хобби

        Приходит
        data:
            "level_name"                - Дополнительное название уровня
            "level_enabled"             - Активен уровень
            "level_title"               - Название уровня
            "level_description"         - Описание уровня
            "level_progress"            - Прогресс прохождения уровня
            "level_image"               - Картинка для главного экрана
            "level_stage"               - Сложность уровня (для сортировки)
            "level_helper_id"           - Ид-шник для хелпера
            "level_background"          - Бекгроунд для главного экрана и просмотра уровня
                "colors"                - 
                "vector"                -

            'level_events'              - список Event уровня
                "event_title"           - Название eventa
                "event_name"            - Дополнительное название eventa  
                "event_description"     - Описание
                "event_image"           - Картинка
                "event_stage"           - Сложность (для сортировки)
                "event_background"      - Бекгроунд (а вдруг потребуется)
                    "colors"            -
                    "vector"            -
                "event_helper_id"       - Ид-шник для хелпера
                "is_completed"          - Завершен event юзером

        notication - код события   
          """)
async def get_user_levels(user_hobby_id: int,
                          user_id: UUID4 = Depends(auth_check_is_user)):
    data = await crud_level.get_user_level(user_id=user_id,
                                           user_hobby_id=user_hobby_id)
    progress = 0.25

    data = list(map(dict, data))

    data = [tuple(groups) for _, groups in groupby(data,
                                                   key=lambda item: item['level_stage'])]
    levels = [
        {'level_enabled': item[0]['level_enabled'],
            'level_title': item[0]['level_title'],
            'level_name': item[0]['level_name'],
            'level_description': item[0]['level_description'],
            'level_image': item[0]['level_image'],
            'level_progress': progress,
            'level_stage': item[0]['level_stage'],
            'level_helper_id': item[0]['level_helper_id'],
            'level_background': {'colors': item[0]['level_colors'],
                                 'vector': item[0]['level_vector']
                                 } if item[0]['level_background_id'] else None,
            'level_events': [
                {
                    'event_title': elem['event_title'],
                    'event_name': elem['event_name'],
                    'event_description': elem['event_description'],
                    'event_image': elem['event_image'],
                    'event_stage': elem['event_stage'],
                    'event_background': {'colors': elem['event_colors'],
                                         'vector': elem['event_vector']
                                         } if elem['event_background_id'] else None,
                    'event_helper_id': elem['event_helper_id'],
                    'is_completed': True if elem['is_completed'] else False,
                }
                for elem in item],
         } for item in data]
    return {'data': levels}




        
