
from fastapi import status, Depends, HTTPException
from pydantic import UUID4
from app.fsm.user_state_machine import UserStateMachine

from typing import List
import datetime


from app.schemas.schema_reflection import SchemaLevelTitle, SchemaReflections
from app.schemas.schema_script import SchemaQuest
from app.utils.const_message import not_found, not_found_time
from app.utils.user_security import auth_check_get_user, auth_check_is_user
from app.crud import crud_reflections, crud_user, crud_script

from app.routes.routes_hobby import hobby


@hobby.get('/reflections-levels/{user_hobby_id}',
           response_model=SchemaReflections,
           status_code=status.HTTP_200_OK,
           dependencies=[Depends(auth_check_get_user)],
           description="""
           Get info reflections of a habie
    РОУТ БЕЗ NOTIFICATION
           Параметры
                * user_hobby_id - ид-шник пользовательского хобби
           Возвращает структуру
                "hobby_id" - ид-шник hobby
                "text"     - текст 
                "complexity" - список уровней
                    [
                        {
                        "level" -       Порядок
                        "title" -       Название
                        "background_color" -  Цвет фона в hex
                        "background_vector" - Направление заливки
                        "text_color"  -       Цвет текста в hex
                        "script" -      Ид-шник главной страницы уровня рефлексии
                        },
                    ]
           """)
async def get_reflections(user_hobby_id: int):
    res = await crud_reflections.get(user_hobby_id)
    if list(res):
        return {'hobby_id': res[0]['hobby_id'], 'text': res[0]['text'],  'complexity': res}


@hobby.get('/reflections-title/{user_hobby_id}',
           response_model=SchemaLevelTitle,
           status_code=status.HTTP_200_OK,
           description="""
            Get info reflections of a habie
            РЕФЛЕКСИЯ ПРИВЫЧКИ
    РОУТ БЕЗ NOTIFICATION
            http://127.0.0.1:8000/hobby/reflections-title/4?script_id=3&date="2020-05-29"
            Параметры
                в запросе
                    * user_hobby_id - ид-шник пользовательского хобби
                в параметрах запроса
                    * script_id - ид-шник Главной страницы уровня сложности
                    * date - текущая дата пользователя

            Возвращает структуру:
                "image"             - ссылку на картинку
                "text_header"       - текст чем и сколько занимался
                "text_title"        - текст о уровне форматированный
                "text_name"         - именнование уровня
                "text_color"        - цвет имени уровня
                "text_description"  - дополнительный текст
                "text_correlation"  - текст приглашение для корреляции с выбранным пользователем временем
                "desired_time"      - сколько планировал в минутах заниматься
                "is_correlation"    - разрешена корреляция
                "correlation"       - значение для корреляции времени
                "max_time"          - максимальное значение коррекции 
                "min_time"          - минимальное значение коррекции

            Если проведена корреляция - надо отправить на бек 
            patch '/properties/{user_hobby_id}'
            body {'long': новое значение }

            По завершению вызывать
                post /user/doing-reflection
           """)
async def get_reflections_title(user_hobby_id: int, script_id: int,
                                date: datetime.date,
                                 user_id: UUID4 = Depends(auth_check_is_user)):
    res = dict(await crud_reflections.get_title(script_id=script_id))
    if not res:
        raise HTTPException(**not_found)
    if (_time := await crud_user.history.get_spent_time(user_id, user_hobby_id, date)) is None:
        raise HTTPException(**not_found_time)
    _time = round(_time/60)
    res['text_header'] = res['text_header'].format(_time)

    if res['is_correlation']:
        res['desired_time'] = await crud_user.properties.get_column(
            user_id=user_id,
            user_hobby_id=user_hobby_id, name='long')
    return res


@hobby.get('/reflections-script/{user_hobby_id}',
           response_model=List[SchemaQuest],
           status_code=status.HTTP_200_OK,
           description="""
            Get info reflections of a habie
            ОПРОСНИК ДЛЯ РЕФЛЕКСИИ ДНЯ
    РОУТ БЕЗ NOTIFICATION
            http://127.0.0.1:8000/hobby/reflections-title/4
            Параметры
                в запросе
                    * user_hobby_id - ид-шник пользовательского хобби

            Возвращает структуру:
                "order"         - порядковый номер вопроса
                "quest_id"      - ид-вопроса
                "quest"         - вопрос
                "answer_type"   - тип ответа, возможные варианты ['yes-no', 'one-choice', 'multi-choices', 'input-text']
                "answer_data"       - Список ответов и их параметры отображения
                                'answer'        - Ответ
                                'answer_colors' - Заливка или цвет ответа
                                'answer_vector' - Вектор Заливки
                                "text_color"  -       Цвет текста в hex
                                'order'         - Порядковый номер ответа
                По завершению вызывать
                post /user/day-reflection
                Который вернет данные для финальной страницы
                """)
async def get_reflections_script(user_hobby_id: int, user_id: UUID4=Depends(auth_check_get_user)):
    script_id = await crud_reflections.get_id_script(user_hobby_id=user_hobby_id)
    data = await crud_script.get_script(script_id=script_id)
    return data
