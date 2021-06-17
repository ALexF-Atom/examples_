from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Union

from app.schemas.custom_type import ImageRichField

class SchemaHobby(BaseModel):
    title: Optional[str]
    description: Optional[str]
    img_icon: Optional[ImageRichField]
    is_enabled: Optional[bool]
    state_icon: Dict

    class Config:
        schema_extra = {
            'example': {
                "title": "Reading a book",
                "description": "helps to understand the world around you better",
                "img_icon": "https://practiqa-media.s3.amazonaws.com/media/media/2021/05/28/reading.svg",
                "is_enabled": True,
                "state_icon": {
                    "disabled": {
                        "colors": [
                            "#B5D8A2"
                        ],
                        "vector": None,
                        "opacity": 1
                    },
                    "enabled": {
                        "colors": [
                            "#86DBCE"
                        ],
                        "vector": None,
                        "opacity": 1
                    }
                },
                "id": 1
            }
        }


class SchemaHobbyModel(SchemaHobby):
    id: int


class SchemaWhat(BaseModel):
    title: str
    example: str
    helper: str
    helper_id: int

    class Config:
        schema_extra = {
            'example': {
                'title': 'What book will you read?',
                'example': 'e.g. islands in the stream by Hemingway',
                'helper': 'what if I don’t know what to read',
                'helper_id': 1,
            }
        }

    @validator("helper", pre=True)
    def process_helper(cls, v):
        return v or ""

    @validator("helper_id", pre=True)
    def process_helper_if(cls, v):
        return v or 0



class SchemaWhere(SchemaWhat):

    answer: List[str]

    class Config:
        schema_extra = {
            'example': {
                'title': 'Where will you read?',
                'example': '',
                'helper': '',
                'helper_id': 0,
                'answer': ["in the living room", "on the sofa",
                            "at the desk in the kitchen", "other"]
            }
        }


class SchemaLong(SchemaWhat):
    complexity_level: Dict[str, Union[str, List[int]]]

    class Config:
        schema_extra = {
            'example': {
                'title': 'For how long will you read?',
                'example': '',
                'helper': '',
                'helper_id': 0,
                'complexity_level': {
                    'low': "Small steps work the best!",
                    'low_value': [1, 3, 5, 10],
                    'medium': "Confident start!",
                    'medium_value': [15, 20, 25],
                    'hard': "Sounds like a challenge! Let’s try!",
                    'hard_value': [30, 35, 40]
                }
            }
        }


class SchemaHobbyProperties(BaseModel):
    hobby_id: int
    what: Optional[SchemaWhat]
    where: Optional[SchemaWhere]
    long: Optional[SchemaLong]



class SchemaHelper(BaseModel):
    hobby_id: int
    title: str
    image: str
    text: str
