from typing import List, Optional
from pydantic import BaseModel
from app.schemas.custom_type import AnswerData, ColorsListBackground



class SchemaQuest(BaseModel):
    quest: str
    answer_data: AnswerData
    quest_id: int
    answer_type: str
    example: Optional[str]
    helper_id: Optional[int]

    class Config:
        schema_extra = {
            'example': {

                "quest": "Have you had the opportunity to do Reading right after turning off the alarm?",
                "answer_data": [
                       {
                           'answer': "Yes",
                           'answer_colors': [],
                           'answer_vector': None,
                           'text_color':'#FFFFFF',
                           'order': 1
                       }
                ],
                "quest_id": 1,
                "order": 1,
                "script_id": 1,
                "helper_id": None,
                "example": None,
                "answer_type": "yes-no",
            }
        }


class SchemaScript(BaseModel):
    script_id: int
    script_title: str
    quests_data: List[SchemaQuest]

    class Config:
        schema_extra = {
            'example': {
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
                                'text_color':'#FFFFFF',
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

            }

        }
