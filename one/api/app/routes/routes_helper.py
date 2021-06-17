
from fastapi import APIRouter, status, Depends
from fastapi.staticfiles import StaticFiles
from typing import Literal
from pydantic import UUID4
from starlette.responses import FileResponse, HTMLResponse

from app.utils.user_security import auth_check_get_user, auth_check_is_user
from app.schemas.schema_helper import NotificationsHelper
from app.settings import TEMPLATES_URL
from app.crud import crud_helper


M_NAME = Literal['what', 'where', 'long']

helper = APIRouter(prefix='/helper', tags=['Helper HTML-VIEW'])

helper.mount(TEMPLATES_URL, StaticFiles(
    directory='templates'), name='templates')


@helper.get('/get/{helper_id}',
            response_model=NotificationsHelper,
            status_code=status.HTTP_200_OK,
            description="""Returns the JSON-view helper of a habie

        title_text:         Optional[str]               "Заголовок"
        head_text:          Optional[str]	            ""
        body_text:          Optional[str]               "Основной текст"
        last_text:          Optional[str]
        image:              Optional[str]               "Изображение"
        button_text:        Optional[str]               "текст-html в кнопке"
        button_font:        Optional[str] 
        button_url:         Optional[str]                "ссылка на ресурс"
        button_id_script:   Optional[str]                "ид-шник на скрипт в приложении"
        button_colors:      Optional[List[str]]          "Список цветов для заливки"
        button_vector:      Optional[str]                "Направление заливки, если два и более цвета в списке"
        open_in_extarnal:   Optional[bool]               "Открыть ссылку во внешнем приложение (true-Да, false-нет)"	
        "button_id":        Optional[int]                "ид-шник кнопки",
                
            """)
async def get_helper(helper_id: int, user_id: UUID4 = Depends(auth_check_is_user)):
    data = await crud_helper.get_id(id=helper_id)
    return {'data': data,
           }

@helper.get('/{model}/{hobby_id}',
            response_class=HTMLResponse,
            deprecated=True,
            status_code=status.HTTP_200_OK,
            description="Returns the HTML-view helper of a habie")
async def get_html_helper(model: M_NAME, hobby_id: int, user_id: UUID4 = Depends(auth_check_is_user)):
    return FileResponse('templates/hobby_helper.html')


@helper.get('/custom-timer',
            status_code=status.HTTP_200_OK,
            description="Returns the data helping of a custom-time")
async def get_helper_custom_timer(user_id: UUID4 = Depends(auth_check_is_user)):
    return {'data': await crud_helper.get('custom-timer'),
   }


@helper.get('/self-reflection',
            status_code=status.HTTP_200_OK,
            description="Returns the data helping of a self-reflection")
async def get_helper_self_reflection(user_id: UUID4 = Depends(auth_check_is_user)):
    return {'data': await crud_helper.get('self-reflection'),
           }

