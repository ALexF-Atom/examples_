from app.schemas.custom_type import ImageRichField, ColorsListBackground, AnswerData
from app.schemas.schema_script import SchemaScript

from pydantic import BaseModel
from typing import List, Dict, Optional, Union


class Background(BaseModel):
    colors: Optional[ColorsListBackground]
    vector: Optional[str]


class SchemaStory(BaseModel):
    id: int
    name: str
    is_active: bool
    duration: int
    preview: ImageRichField
    preview_colors: Optional[ColorsListBackground]

    preview_vector: Optional[str]
    text_preview: Optional[str]
    like_is: Optional[bool]

    class Config:
        schema_extra = {
            'example': {
                "id": 5,
                "name": "five",
                "is_active": False,
                "duration": 15,
                "preview": "https://practiqa-media.s3.amazonaws.com/media/media/2021/05/25/help.jfif",
                "preview_colors":  ["#F9E285","#6FCEC0"],
                "preview_vector": "90",
                "like_is": None
            }
        }


class NotificationSchemaStory(BaseModel):
    data: List[SchemaStory]
    


class StoryContent(BaseModel):
    id: int
    order: int
    content: ImageRichField
    content_text: Optional[str]
    content_colors: ColorsListBackground

    content_vector: Optional[str]
    content_position: Optional[str]

    button_text: Optional[str]
    button_font: Optional[str]
    button_background: Optional[Background]
    button_url: Optional[str]
    button_id_script: Optional[str]
    button_position: Optional[str]
    button_id: Optional[int]

    script_data: Optional[SchemaScript]
    script_title_position: Optional[str]
    as_view_script: Optional[str]

    is_share: bool
    share_image: ImageRichField

    class Config:
        schema_extra = {
            'example':{   
                "id" : 1,
                "order": 1,
                "content": "https://practiqa-media.s3.amazonaws.com/media/media/2021/05/25/help.jfif",
                "content_text": "<p>Love</p>",
                "content_position": "top",
                "content_colors":  ["#FFFFFF"],
                "content_vector": None,     
                "button_text": None,
                "button_font": None,
                "button_colors": None,
                "button_vector": None,
                "button_url": None,
                "button_id_script": None,
                "button_position": None,
                "button_id": None,
                'script_data': {
                    'script_id': 1,
                    'script_title': "You Want Read?",
                    'quests_data': [
                        {
                            "quest": "Have you had the opportunity to do Reading right after turning off the alarm?",
                            "answer_data": [
                                {
                                    'answer': "Yes",
                                    'answer_colors': [],
                                    'answer_vector': None,
                                    'text_color': "#FFFFFF",
                                    'order': 1
                                }
                            ],
                            "quest_id": 1,
                            "order": 1,
                            "script_id": 1,
                            "helper_id": None,
                            "example": None,
                            "answer_type": "yes-no",
                        },

                    ]

                },

                "script_title_position": "center",
                "as_view_script": "range",
                
                "is_share": False,
                "share_image": ""


            }
        }
