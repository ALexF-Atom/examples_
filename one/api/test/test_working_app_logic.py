import datetime
from typing import Dict, List, NoReturn, Tuple
from pydantic import UUID4
from app.fsm.user_state_machine import UserStateMachine
from fastapi import status
import pytest
from httpx import AsyncClient
from pprint import pprint
# from itertools import groupby

from main import app
from app.models.base import db
from app.crud import crud_hobby, crud_reflections, crud_user, crud_story
# from app.schemas.schema_user.statistics import HobbyStatistics, ReflectionStatistic, TitleRoutine
from .json_data import (data_hobby_properies, data_hobby,
                        user_data, user_history, user_alarm,
                        user_reflections_hobby, user_reflections_day)
from .json_story import stories

FOR_RESPONSE = Tuple[AsyncClient, int, Dict[Dict, UUID4]]

QUANT = 100



async def create_data(client, data_hobby_properies: Dict, data_hobby: Dict) -> int:
    headers = {'secret_uid': 'secret'}

    # Создание привычки
    response = await client.post('/admin/create-hobby', json=data_hobby, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['id'] in [1, 2]
    # Подготовка данных свойств привычки
    data_hobby_properies['hobby_id'] = response.json()['id']
    # Сохранение свойств привычки
    response = await client.post('/admin/create-hobby-properties', json=data_hobby_properies, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    hobby_id = response.json()['id']
    assert hobby_id in [1, 2]
    # проверка сохраненных свойств привычки
    title = (await crud_hobby.get_what(hobby_id))['title']
    assert title == data_hobby_properies['what']['title']
    return hobby_id


async def create_user(client: AsyncClient) -> Dict[Dict, UUID4]:
    response = await client.post('/user/create')
    assert response.status_code == status.HTTP_201_CREATED
    return {'secret_uid': response.json()['uid']}


async def create_user_properties(client: AsyncClient, hobby_id: int,
                                 user_data: Dict, headers: Dict[Dict, UUID4]) -> int:
    user_data['hobby_id'] = hobby_id
    response = await client.post('/user/properties', json=user_data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    user_hobby_id = response.json()['data']['user_hobby_id']
    assert user_hobby_id in [1, 2]
    return user_hobby_id


async def get_all_hobby(client: AsyncClient, headers: Dict[Dict, UUID4]) -> NoReturn:
    response = await client.get('/user/hobby', headers=headers)
    user_hobbies = response.json()['data']
    assert len(user_hobbies) == 1


async def update_user_properties(for_response: FOR_RESPONSE, user_data: Dict) -> NoReturn:
    client, user_hobby_id, headers = for_response
    response = await client.patch(f'/user/properties/{user_hobby_id}', json=user_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['data']['id'] == user_hobby_id


async def get_user_properties(for_response: FOR_RESPONSE, user_data: Dict) -> int:
    client, user_hobby_id, headers = for_response
    response = await client.get(f'/user/properties/{user_hobby_id}', headers=headers)
    user_hobby = response.json()['data']
    assert user_hobby['what'] == user_data['what']
    return user_hobby


async def get_alarm(for_response: FOR_RESPONSE, user_alarm: Dict) -> NoReturn:
    client, user_hobby_id, headers = for_response
    response = await client.get(f'/user/alarm/{user_hobby_id}', headers=headers)
    alarm = response.json()['data']
    assert alarm == user_alarm
    assert alarm['time'] == user_alarm['time']
    assert alarm['notification'] == user_alarm['notification']


async def update_alarm(for_response: FOR_RESPONSE, user_alarm: Dict) -> NoReturn:
    client, user_hobby_id, headers = for_response
    response = await client.patch(f'/user/alarm/{user_hobby_id}', json=user_alarm, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['data']['id'] == user_hobby_id


async def create_final():
    data = {
        'image': 'image',
        'text': 'Very Cool'
    }
    id_ = await crud_reflections.save_final(data)
    assert id_ == 1


async def save_reflections_history(for_response: FOR_RESPONSE, user_reflections: Dict):
    client, user_hobby_id, headers = for_response
    response = await client.post(f'/user/doing-reflection', json=user_reflections, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['data']['id'] in range(QUANT)


async def save_reflections_day(for_response: FOR_RESPONSE, user_reflections_day: Dict):
    client, user_hobby_id, headers = for_response
    response = await client.post(f'/user/day-reflection', json=user_reflections_day, headers=headers)
    assert response.json()['data']['text'] == 'Very Cool'
    assert response.json()['data']['image'] == 'image'


async def get_statistics_hobies(for_response: FOR_RESPONSE, date:datetime.date, delta: int):
    client, user_hobby_id, headers = for_response
    params = {'date': date, 'delta': delta}
    response = await client.get('/user/my-statistics/', headers=headers, params=params)
    return response


async def get_reflections_history(for_response: FOR_RESPONSE, start: datetime.date, end: datetime.date):
    client, user_hobby_id, headers = for_response
    params = {'start': start, 'end': end}
    response = await client.get('/user/history-reflection_v2', headers=headers, params=params)
    return response


async def get_stories(for_response: FOR_RESPONSE):
    client, user_hobby_id, headers = for_response
    response = await client.get('/story/all', headers=headers)
    # assert response.status_code == status.HTTP_200_OK
    return response


@pytest.mark.asyncio
async def test_logic_app(db_test,
                         data_hobby_properies=data_hobby_properies,
                         data_hobby=data_hobby,
                         user_data=user_data,
                         user_alarm=user_alarm,
                         user_history=user_history,
                         user_reflections=user_reflections_hobby,
                         user_reflections_day=user_reflections_day):
    await db.connect()
    async with AsyncClient(app=app, base_url="http://test") as app_test:
        hobby_id = await create_data(app_test, data_hobby_properies[0], data_hobby[0])

        headers = await create_user(app_test)
        user_hobby_id = await create_user_properties(app_test, hobby_id=hobby_id, user_data=user_data, headers=headers)

        await get_all_hobby(app_test, headers=headers)

        for_response: FOR_RESPONSE = [app_test, user_hobby_id, headers]

        await get_user_properties(for_response, user_data=user_data)

        user_data['where'] = "beach"
        await update_user_properties(for_response, user_data=user_data)
        await get_user_properties(for_response, user_data=user_data)

        await get_alarm(for_response, user_alarm=user_alarm)

        user_alarm['time'] == "09:41:00"
        await update_alarm(for_response, user_alarm=user_alarm)
        await get_alarm(for_response, user_alarm=user_alarm)

        user_alarm['notification'] = True
        await update_alarm(for_response, user_alarm=user_alarm)
        await get_alarm(for_response, user_alarm=user_alarm)

        user_history['user_hobby_id'] = user_hobby_id

        await create_final()

        data_hobby['title'] = "Writing a book"
        hobby_id = await create_data(app_test, data_hobby_properies, data_hobby)
        user_hobby_id_two = await create_user_properties(app_test, hobby_id=hobby_id, user_data=user_data, headers=headers)

        base = datetime.datetime.today()
        date_list = [base + datetime.timedelta(days=x) for x in range(QUANT)]

        for i, date in enumerate(date_list, start=1):
            user_history['date'] = str(date.date())
            user_history['spent_time'] += 10
            user_history['user_hobby_id'] = user_hobby_id
            response = await app_test.post('/user/doing-routine', json=user_history, headers=headers)
            assert response.status_code == status.HTTP_201_CREATED

            if i % 4 == 0:
                user_reflections['date'] = str(date.date())
                user_reflections['user_hobby_id'] = user_hobby_id
                await save_reflections_history(for_response, user_reflections)

            if i % 2 and i != 1:
                user_history['user_hobby_id'] = user_hobby_id_two
                response = await app_test.post('/user/doing-routine', json=user_history, headers=headers)

                user_reflections['date'] = str(date.date())
                user_reflections['user_hobby_id'] = user_hobby_id_two
                await save_reflections_history(for_response, user_reflections)

            if i % 3:
                user_reflections_day['date'] = str(date.date())
                await save_reflections_day(for_response, user_reflections_day)

        assert user_history['spent_time'] == await crud_user.history.get_spent_time(
            user_hobby_id=user_hobby_id,
            date=datetime.datetime.strptime(user_history['date'], '%Y-%m-%d'))

        user_id = headers['secret_uid']

        response = await get_statistics_hobies(for_response, date_list[-1].date(), 5)


    await db.disconnect()
