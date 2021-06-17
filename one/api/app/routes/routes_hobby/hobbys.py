from fastapi import status, Depends
from typing import List
from itertools import groupby

from app.utils.user_security import auth_check_get_user
from app.schemas.schema_hobby import SchemaHobbyModel, SchemaHobbyProperties
from app.crud import crud_hobby

from app.routes.routes_hobby import hobby


@hobby.get('/all',
           response_model=List[SchemaHobbyModel],
           status_code=status.HTTP_200_OK,
           dependencies=[Depends(auth_check_get_user)],
           description="""Info all hobbys
           РОУТ БЕЗ NOTIFICATION

           Приходит
           id                   - ид-шник хобби
           title                - название хобби
           description          - описание хобби
           is_enabled           - активно ли хобби для выбора
           img_icon             - иконка для хобби в svg
           state_icon           - описание состояний иконки для цвета с ключами
                disabled            - состояние disabled
                    colors              - список цветов
                    vector              - направление градиента
                    opacity             - alfa-канал для цвета (от 0 до 1)
                enabled             - состояни enabled
                    colors              - список цветов
                    vector              - направление градиента
                    opacity             - alfa-канал для цвета (от 0 до 1)
           """,)
async def hobby_all():
    data = await crud_hobby.all()
    data = [tuple(groups) for _, groups in groupby(data, key=lambda item: item['id'])]

    data = [
        {   'id': item[0]['id'],
            'title': item[0]['title'],
            'description': item[0]['description'],
            'is_enabled': item[0]['is_enabled'],
            'img_icon': item[0]['img_icon'],
            'state_icon': {
                
                    elem['title_state']: {
                    'colors': elem['colors'],
                    'vector': elem['vector'],
                    'opacity': elem['opacity']
                    }
                for elem in item}
            
        }
    for item in data
    ]
    return data


@hobby.get('/properties/{hobby_id}',
           response_model=SchemaHobbyProperties,
           status_code=status.HTTP_200_OK,
           dependencies=[Depends(auth_check_get_user)],
           description="""Returns the properties of a habiе
           РОУТ БЕЗ NOTIFICATION""",
           )
async def properties_get(hobby_id: int):
    return {'hobby_id': hobby_id,
            'what': await crud_hobby.get_what(hobby_id=hobby_id),
            'where': await crud_hobby.get_where(hobby_id=hobby_id),
            'long': await crud_hobby.get_long(hobby_id=hobby_id)}
