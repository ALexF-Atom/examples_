from pydantic import BaseModel
from typing import  Optional, List

from app.schemas.custom_type import ImageRichField

class SchemaHelper(BaseModel):
    title_text: Optional[str]
    head_text: Optional[str]
    body_text: Optional[str]
    last_text: Optional[str]
    image: Optional[ImageRichField]

    button_text: Optional[str]
    button_url: Optional[str]
    button_id_script: Optional[str]
    button_colors: Optional[List[str]]
    button_vector: Optional[str]
    button_id: Optional[int]
    open_in_extarnal: Optional[bool]


    class Config:
        schema_extra = {
            "title_text": "Заголовок",
            "head_text": "",
            "body_text": "Основной текст",
            "last_text": "",
            "image": "Изображение",
            "button_text": "текст-html в кнопке",
            "button_colors": "Список цветов для заливки",
            "button_vector": "Направление заливки, если два и более цвета в списке",
            "button_id_script": "ид-шник на скрипт в приложении",
            "button_url": "ссылка на ресурс",
            "button_id": "ид-шник кнопки",
            "open_in_extarnal": "Открыть ссылку во внешнем приложение (true-Да, false-нет)"
        }


class NotificationsHelper(BaseModel):
    data: SchemaHelper
    
