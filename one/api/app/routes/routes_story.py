from typing import List
from fastapi import APIRouter, status, Depends
from pydantic.types import UUID4
from app.fsm.user_state_machine import UserStateMachine

from app.utils.user_security import auth_check_get_user, auth_check_is_user

from app.crud import crud_story, crud_script
from app.schemas.schema_story import NotificationSchemaStory, StoryContent
from app.schemas.schema_message import NotificationCreate, NotificationUpdate
from app.schemas.schema_user import SchemaUserStory, SchemaViewStory, SchemaLikeStory

story = APIRouter(prefix='/story', tags=['STORIES'])


@story.get('/all/{user_hobby_id}',
           response_model=NotificationSchemaStory,
           status_code=status.HTTP_200_OK,
           description="""
    Ожидает
            user_hobby_id               - ид-шник пользовательского хобби

    Приходит упорядоченные стори (сначала всегда идут непросмотренные в определенном порядке, потом просмотренные)
    data - данные для работы: >>    
            "id"                        - ид-шник стори
            "name"                      - название стори
            "duration"                  - длительность показа стори в секундах
            "is_active"                 - просмотрена ли картинка
                                                True - не просмотрена
                                                False - просмотрена
            "like_is"                   - состояние Like-Dislike.
                                            Если равна null, то нет лайка и нет дизлайка
                                            Если равна true, то поставил лайк
                                            Если равна false, то поставил дизлайк
        Cториз                       
            "preview"                   - картинка
            'preview_colors'            - список цветов для бекграунда
            'preview_vector'            - направление градиента 
            "text_preview"              - текст в формате html          
    
                       
""")
async def get_all(user_hobby_id: int,
                  user_id: UUID4 = Depends(auth_check_is_user)):
    stories = await crud_story.get(user_id)
    return {'data': stories}


@story.get('/content/{story_id}',
           response_model=List[StoryContent],
           status_code=status.HTTP_200_OK,
           description="""
           Контент приходит упорядоченный, доп обработка не требуется
     Развенутый контент сториз
            "id"                        - ид-контента
            "order"                     - порядковый номер  

            "content"                   - картинка развернутого стори (контент)

            "content_text"              - текст в формате html
            "content_position "
            'content_colors'            - список цветов для заливки контента
            'content_vector'            - направление градиента
            
            "button_text"               - текст кнопки в формате html   
            'button_colors'             - список цветов для заливки кнопки
            'button_vector'             - направление градиента
            "button_url"                - ссылка  
            "button_id_script"          - ид-шник скрипта
            "button_position"           - позиция кнопки ['bottom', 'center', 'top']
            "button_id"                 - "ид-шник кнопки",
            
            'script_data'               - информация вопросник
                    'script_id'         - ид-шник опросника
                    'script_title'      - Название опросника
                        'quests_data'           - Список вопросов и их параметры 
                            "quest"             - Сам вопрос
                            "answer_data"       - Список ответов и их параметры отображения
                                'answer'        - Ответ
                                'answer_colors' - Заливка или цвет ответа
                                'answer_vector' - Вектор Заливки
                                'text_color'    - Цвет текста
                                'order'         - Порядковый номер ответа
                        "quest_id"      - ид -вопроса
                        "order"         - порядковый номер вопроса
                        "helper_id"     - ид-шник хелпера для вопроса
                        "example"       - Пример ответа, если ожидеатся пользовательский ввод
                        "answer_type"   - Тип ответа ['one-choice', 'multi-choice', 'input-answer', 'yes-no']
            "script_title_position"      - позиция вопроса на экране
            
            "as_view_script"            - как отображать вопрос ['list', 'range']

            "is_share"                  - разрешено ли шаринг
            "share_image"               - картинка для шаринга

            ВНИМАТЕЛЬНО!
            если есть button - ОБЯЗАТЕЛЬНО ПОВЕСИТЬ НА НЕЕ /user/action/{button_id}
            если есть script - ОБЯЗАТЕЛЬНО ПОВЕСИТЬ НА НЕГО /user/save-quiz/{script_id}
            если есть helper - ОБЯЗАТЕЛЬНО ПОВЕСИТЬ НА НЕГО /helper/get/{helper_id}
                если у helper есть button - ОБЯЗАТЕЛЬНО ПОВЕСИТЬ НА НЕЕ /user/action/{button_id} 
    """)
async def get_content_story(story_id: int,  user_id: UUID4 = Depends(auth_check_is_user)):

    content = await crud_story.get_content(story_id)
    for item in content:
        if item['script_id']:
            data = await crud_script.get_script(item['script_id'])
            
            item['script_data'] = {'script_id': item['script_id'],
                                   'script_title': data[0]['script_title'],
                                   'quests_data': data}

    return content


@story.post('/view/{story_id}',
            response_model=NotificationCreate,
            status_code=status.HTTP_201_CREATED,
            description="""
    Cохранение состояния о просмотре стори
    Ожидаемые параметры:
        story_id  - ид-шник стори

    Необязательные параметры
        view_time - сколько просматривал в секундах стори
        view_at   - время просмотра 2021-05-19 15:40
""")
async def save_view(story_id: int, data: SchemaViewStory,
                     user_id: UUID4 = Depends(auth_check_is_user)):
    if await crud_story.is_view(user_id=user_id, story_id=story_id):
        message = f"Attention! Story {story_id} viewed again by the user"
        return {'data': {'id': story_id,
                         'message': message}}

    data = data.dict(exclude_unset=True)
    data.update(user_id=user_id, story_id=story_id)
    story_id = await crud_story.save(data)

    return {'data': {'id': story_id}}


@story.patch('/update/{story_id}',
             response_model=NotificationUpdate,
             status_code=status.HTTP_201_CREATED,
             description="""        
        Cохранение взаимодействия пользователя со стори
        Ожидаемые параметры:
        story_id  - ид-шник стори

        Остальные перечисленные ниже параметры - опциональны, но не забудьте о логике человеческой

        like_is   - Перезаписываем текущее состояние (явно передаем состояние лайка-дизлайка стори)
            Это не обработка клика на кнопку Лайка-Дизлайка
            Это запись результата после клика - состояние вычисляется на стороне клиента
                        Если Dislike, отправляем (-1)
                        Если Like, отправляем (1)
                        Если нет Dislike и нет Like (0) 
        like_at   - время нажатие на лайк/дизлайк 2021-05-19 15:40
        
        view_time - сколько просматривал в секундах стори
        view_at   - время просмотра 2021-05-19 15:40
        
        share_is  - если расшарил, отправляем True
        share_at  - время шаринга 2021-05-19 15:40
        
""")
async def update_story(story_id: int, data: SchemaUserStory,
                        user_id: UUID4 = Depends(auth_check_is_user)):
    data = data.dict(exclude_unset=True)
    if data.get('like_is') is not None:
        values = {1: True, -1: False, 0: None}
        data['like_is'] = values[data['like_is']]

    return {'data': {'id': await crud_story.update(user_id=user_id, story_id=story_id, data=data)},
           }


@story.patch('/like-dislike/{story_id}',
             response_model=NotificationUpdate,
             status_code=status.HTTP_201_CREATED,
             description="""        
        Like/Dislike
        Не обращая на текущее состояние
        РЕАКЦИЯ НА НАЖАТИЕ КНОПКИ
            т.е. результат вычисляется на стороне бека
        Ожидаемые параметры:
        story_id  - ид-шник стори

        like_is   - Допустимые значения  
                        Если нажали на кнопку Dislike, отправляем - (-1)
                        Если нажали на кнопку Like, отправляем - (1) 
        like_at   - время нажатие на лайк/дизлайк 2021-05-19 15:40
        
""")
async def like_dislike(story_id: int, data: SchemaLikeStory,
                        user_id: UUID4 = Depends(auth_check_is_user)):
    data = data.dict(exclude_unset=True)
    values = {1: True, -1: False}
    data['like_is'] = values.get(data['like_is'])

    like_is = await crud_story.get_is_like(user_id=user_id, story_id=story_id)
    if like_is == data['like_is']:
        data['like_is'] = None

    story_id = await crud_story.update(user_id=user_id, story_id=story_id, data=data)

    return {
        'data': {'id': story_id}
        }
