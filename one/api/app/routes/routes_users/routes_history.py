
from app.crud.crud_user import history
from typing import List
from app.schemas.schema_user.history import SchemaAnswer
from app.schemas.schema_script import SchemaScript
from fastapi import status, Depends, HTTPException
from pydantic import UUID4
from app.fsm.user_state_machine import UserStateMachine
from itertools import groupby
import datetime

from app.schemas.schema_reflection import NotificationReflectionFinal
from app.schemas.schema_message import NotificationCreate
import app.schemas.schema_user as sch
from app.utils.user_security import auth_check_get_user, auth_check_is_user
from app.crud import crud_user, crud_reflections,crud_level, crud_script

from app.routes.routes_users import user
from random import randint

@user.post('/doing-routine',
           response_model=NotificationCreate,
           status_code=status.HTTP_201_CREATED,
           responses={404: {"description": "The item was not found"}},
           description="""
              Keeping the routine running
    data - данные для работы: >>
        *  user_hobby_id - ид-шник пользовательского хобби
        *  date -          дата выполнения в формате год-месяц-день например '2021-05-28'
        *  actual_time -   в какое время начал выполнение в формате час(0-24):минута(0-60)  например'9:41'
        *  planned_time -  восколько планировал начать выполнение в формате как и actual_time
                           параметр необязательный, может быть вычислен на беке
        *  spent_time -    сколько выполнял рутину в секундах
        *  desired_time -  сколько планировал выполнять рутину в секундах
                           параметр необязательный, может быть вычислен на беке
                           
    
                           """)
async def save_doing_routine(data: sch.SchemaUserHobbyHistory,
                              user_id: UUID4 = Depends(auth_check_is_user)):
    if not await crud_user.hobby.auth_is_user_hobby_id(user_id, data.user_hobby_id):
        raise HTTPException(status_code=404, detail="User hobby not found")

    if data.planned_time is None:
        data.planned_time = await crud_user.alarm.get_column(
            user_id=user_id,
            user_hobby_id=data.user_hobby_id,
            name='time')
    if data.desired_time is None:
        data.desired_time = await crud_user.properties.get_column(
            user_id=user_id,
            user_hobby_id=data.user_hobby_id,
            name='long')
    return {'data': {'id': await crud_user.history.save_hobby(user_id=user_id,
                                                              history=data.dict())},
            }



@user.post('/doing-reflection',
           response_model=NotificationCreate,
           responses={404: {"description": "The item was not found"}},
           status_code=status.HTTP_201_CREATED,
           description="""
              Keeping the routine running
              CОХРАНЕНИЕ ДАННЫХ РЕФЛИКСИИ ПРИВЫЧКИ
    data - данные для работы: >>
        * user_hobby_id     - ид-шник пользовательского хобби
        * date              - дата выполнения в формате год-месяц-день например '2021-05-28'
        * is_correlation    - проводил ли корреляцию времени выполнения
        * correllation      - значение корреляции (параметр необязательный)
        * level             - выбранный уровень (Light, Hard)
    
    
        """)
async def save_doing_reflection(data: sch.SchemaUserReflectionHistoryHobby,
                                 user_id: UUID4 = Depends(auth_check_is_user)):
    if not await crud_user.hobby.auth_is_user_hobby_id(user_id, data.user_hobby_id):
        raise HTTPException(status_code=404, detail="User hobby not found")

    history_id = await crud_user.history.save_reflections(user_id=user_id,
                                                          history=data.dict())
   
    return {'data': {'id': history_id}}



@user.post('/day-reflection',
           response_model=NotificationReflectionFinal,
           responses={404: {"description": "The item was not found"}},
           status_code=status.HTTP_201_CREATED,
           description="""
              Keeping the routine running
              РЕФЛИКСИЯ ДНЯ CОХРАНЕНИЕ ДАННЫХ
    data - данные для работы: >>  
        * date              - дата выполнения в формате год-месяц-день например '2021-05-28'
        * answers           - список ответов на вопросы [{'quest_id': int, 'answer': str }]
    
    
        """)
async def save_day_reflection(data: sch.SchemaUserReflectionsHistoryDay,
                               user_id: UUID4 = Depends(auth_check_is_user)):
    ref_id = await crud_user.history.save_reflections_day(user_id=user_id,
                                                          history=data.dict())

    return {'data': await crud_reflections.get_final(final_id=1),}



@user.get('/history-hobby',
          response_model=sch.NotificationDetailHobby,
          status_code=status.HTTP_200_OK,
          description="""
            hobby statistics for the selected period
            Отдает статистику историю  развития всех хобби пользователя
        data - данные для работы: >>
            Ожидаемые параметры в запросе
            *  start -        дата первого дня в формате год-месяц-день 
            *  end -          дата последнего дня в формате год-месяц-день 
            Например start='2021-05-01' по с end='2021-05-31' вернет статистику за месяц
            Проверка на дурака не включена, если даты не логичны, вернется пустой список.

            Приходят
            "path"
            "productivity"
            "text"
                "title"
                "text"
            "next_level"
            "how_days"

            Данные по рутине
            'routine'           - список рутин со следующими ключами
                'title'         - название хобби
                'long'          - актуальные данные продолжительности времени развития привычки в секундах
                'user_hobby_id' - ид-шник пользовательского хобби
                'hobby_id'      - ид-шник хобби глобальный
                'statistic' - список по дням, со следующими данными
                    [
                        "date"          - дата из выбранного периода
                        "actual_time"   - во сколько выполнял рутину
                        "planned_time"  - во сколько планировал выполнять
                        "spent_time"    - сколько выполнял в этот день
                        "desired_time"  - сколько планировал выполнять
                    ]
        
        
        

        ** Важно Если активности не было за выбранный период то
                                    'statistic' =  []
                """)
async def get_statistics_hobby(start: datetime.date,
                               end: datetime.date,
                                user_id: UUID4 = Depends(auth_check_is_user)):
    mock_data = {
        'path': 0.02,
        'productivity': 0.15,
        'text': {
            'title': 'Key insights',
            'text': 'If your view of the world comes from watching the news and reading newspapers, you could be forgiven for lying awake at night worrying about the future.'
        },
        'next_level': 2,
        'how_days': 10
    }
    routine = await crud_user.statistic.get_hobies(user_id=user_id, start=start, end=end)

    routine = [
        {**mock_data,
            'user_hobby_id': item[0]['user_hobby_id'],
            'hobby_id': item[0]['hobby_id'],
            'title': item[0]['title'],
            'long': item[0]['long'],
            'name': item[0]['name'],
            'statistic': [
                {
                    'date': stat['date'],
                    'actual_time': stat['actual_time'],
                    'planned_time': stat['planned_time'],
                    'spent_time': stat['spent_time'],
                    'desired_time': stat['desired_time']
                }
                for stat in item
            ]
         }
        for item in [tuple(groups) for _, groups in groupby(routine,
                                                            key=lambda item: item['user_hobby_id'])]
    ]

    return {'data': routine}



@user.get('/my-statistics',
          response_model=sch.NotificationUserStatistics,
          status_code=status.HTTP_200_OK,
          description="""
            hobby statistics for the selected period
            Для главного экрана. Отдает сводную статистику. Одним запросом.
        'progress': 0.01,
        'level_title': "Level 1: Wave of Enthusiasm",
        'level_image': "http://",
        'level_colors': ['#A78AAA','#B81000'],
        'level_vector': 90,
        data - данные для работы: >>
            Данные по рутине
                'routine'           - список рутин со следующими ключами
                    'title'         - название хобби
                    'long'          - актуальные данные продолжительности времени развития привычки в секундах
                    'user_hobby_id' - ид-шник пользовательского хобби
                    'hobby_id'      - ид-шник хобби глобальный
                    'statistic' - список по дням, со следующими данными
                       [
                            "date"          - дата из выбранного периода
                            "actual_time"   - во сколько выполнял рутину
                            "planned_time"  - во сколько планировал выполнять
                            "spent_time"    - сколько выполнял в этот день
                            "desired_time"  - сколько планировал выполнять
                       ]

            ** Важно Если активности не было за выбранный период то
                                        'statistic' =  []

            Рефлексия у нас двух типов - хобби и дня, возвращаю
                'reflection'            - рефлексия, со следующимим ключами
                    'total_user_hobby'  - сколько хобии (и соответсвенно каждой рефлексии)
                    'title'             - 'Self-reflection',
                    'long':             -  воемя выполнения в секундах,
                    'statistic'         - список по дням, со следующими данными
                        [
                            "date"          - дата из выбранного периода
                            "day"           - пройдена ли рефлексия дня (1 пройдена, 0 не пройдена)
                            "hobby"         - спискок user_hobby_id по которым пройдена рефлексия
                        ]
        
        
                        
            Ожидаемые параметры в запросе
            *  date          - текущая дата на пользовательском устройстве в формате год-месяц-день например '2021-05-28'
            *  delta         - на сколько дней за прошлый период идем вниз. В MVP это значение равно 7
                    """)
async def get_my_statistics(date: datetime.date,
                            delta: int,
                             user_id: UUID4 = Depends(auth_check_is_user)):

    start = date - datetime.timedelta(days=delta)
    routine = await crud_user.statistic.get_hobies(user_id=user_id,
                                                   start=start, end=date)
    level_info = await crud_level.current_user_level(user_id, 1)

    mock_data = {
        'progress': randint(1,100)/100,
        'level': "Level 1: Wave of Enthusiasm",
    }
    

    routine = [
        {
            'user_hobby_id': item[0]['user_hobby_id'],
            'hobby_id': item[0]['hobby_id'],
            'title': item[0]['title'],
            'long': item[0]['long'],
            'name': item[0]['name'],
            'statistic': [
                {
                    'date': stat['date'],
                    'actual_time': stat['actual_time'],
                    'planned_time': stat['planned_time'],
                    'spent_time': stat['spent_time'],
                    'desired_time': stat['desired_time']
                }
                for stat in item
            ]
        }
        for item in [tuple(groups) for _, groups in groupby(routine,
                                                            key=lambda item: item['user_hobby_id'])]
    ]

    reflection = {
        'total_user_hobby': await crud_user.hobby.count(user_id=user_id),
        'statistic': await crud_user.statistic.get_reflection(user_id=user_id,
                                                              start=start,
                                                              end=date)
    }

    # добавить FSm

    return {'data': {**mock_data, **level_info, 'routine': routine, 'reflection': reflection},
            }



@user.get('/history-reflection',
          response_model=sch.NotificationDetailReflection,
          status_code=status.HTTP_200_OK,
          description="""
            hobby statistics for the selected period
            Отдает статистику истории РЕФЛЕКСИИ
        data - данные для работы: >>
        

            Ожидаемые параметры в запросе
                *  start         - дата первого дня в формате год-месяц-день 
                *  end           - дата последнего дня в формате год-месяц-день 
            Например start='2021-05-01' по с end='2021-05-31' вернет статистику за месяц
            Проверка на дурака не включена, если даты не логичны, вернется пустой список.

                    """)
async def get_statistics_reflection(start: datetime.date,
                                    end: datetime.date,
                                     user_id: UUID4 = Depends(auth_check_is_user)):
    mock_data = {
        'path': 0.02,
        'productivity': 0.15,
        'text': {
            'title': 'Key insights',
            'text': 'If your view of the world comes from watching the news and reading newspapers, you could be forgiven for lying awake at night worrying about the future.'
        },
        'next_level': 2,
        'how_days': 10,
        'button': {
            'text': 'talk to a habit coach',
            'url': 'https://google.com'
        },

    }
    reflection = {
        'total_user_hobby': await crud_user.hobby.count(user_id=user_id),
        'statistic': await crud_user.statistic.get_reflection_v2(user_id=user_id,
                                                                 start=start, end=end)
    }

    return {'data': {**mock_data, 'reflection': reflection},
            }


@user.get('/quiz/{script_id}',
          status_code=status.HTTP_200_OK,
          response_model=SchemaScript,
          description="""
        Возвращает односложный скрипт
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
                    """)
async def get_quiz_data(script_id: int,
                         user_id: UUID4 = Depends(auth_check_is_user)):
    return await crud_script.get_script(script_id=script_id)


@user.post('/save-quiz/{script_id}',
           status_code=status.HTTP_201_CREATED,
           response_model=NotificationCreate,
           description="""
                Сохраняет ответы пользователя анкеты
                    """)
async def save_answer_quiz(script_id: int, answers: List[SchemaAnswer],
                            user_id: UUID4 = Depends(auth_check_is_user)):

    return {'data': {'id': script_id},
            }
