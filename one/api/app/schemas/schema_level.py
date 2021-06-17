from pydantic import BaseModel
from typing import List, Optional
from app.schemas.custom_type import ImageRichField, ColorsListBackground


from app.schemas.schema_story import Background


class SchemaAchievment(BaseModel):
    achievement_id: int
    achievement_image: Optional[ImageRichField]
    navigation_title: Optional[str]
    position_image: Optional[str]
    share_image: Optional[ImageRichField]
    achievement_title: Optional[str]
    achievement_text: Optional[str]
    achievement_colors: Optional[ColorsListBackground]
    button_id: Optional[int]
    achievement_vector: Optional[str]
    button_text: Optional[str]
    position_button: Optional[str]
    button_url: Optional[str]
    button_id_script: Optional[int]
    button_colors: Optional[ColorsListBackground]

    button_vector: Optional[str]

    class Config:
        schema_extra = {
            'example': {
                "achievement_id": 1,
                "navigation_title": "You've unlocked a new event",
                "achievement_image": "https://practiqa-media.s3.amazonaws.com/media/media/2021/05/25/image1_VCHGEie.png",
                "position_image": "center",
                "achievement_text": "<p>You&#39;ve had 3 days in full observYou've unlocked a new eventa,nce</p>",
                "achievement_title": "<p>Congrat!</p>",
                "share_image": "https://practiqa-media.s3.amazonaws.com/media/media/2021/05/25/image1_VCHGEie.png",
                "position_button": "bottom",
                "achievement_colors": None,
                "achievement_vector": None,
                "button_id": None,
                "button_text": None,
                "button_url": None,
                "button_id_script": None,
                "button_colors": None,
                "button_vector": None
            }
        }


class Event(BaseModel):
    event_title: str
    event_name: Optional[str]
    event_description: str
    event_image: ImageRichField
    event_stage: int

    event_background: Optional[Background]
    event_helper_id: Optional[int]
    is_completed: bool

    class Config:
        schema_extra = {
            'example': {
                "event_title": "Event 6",
                "event_name": "Event 6",
                "event_description": "Text6",
                "event_image": "https://practiqa-media.s3.amazonaws.com/media/media/2021/05/25/help.jfif",
                "event_stage": 6,
                "event_background": {
                    "colors": [
                        "#F9E285",
                        "#6FCEC0"
                    ],
                    "vector": "90"
                },
                "event_helper_id": None,
                "is_completed": False
            }
        }


class Level(BaseModel):
    level_enabled: bool
    level_name: Optional[str]
    level_title: str
    level_description: str
    level_progress: float
    level_stage: int
    level_background: Optional[Background]
    level_image: ImageRichField
    level_helper_id: Optional[int]
    level_events: List[Event]

    class Config:
        schema_extra = {
            'example': {
                "level_name": None,
                "level_enabled": True,
                "level_title": "Level 2: The name of a level",
                "level_description": "To make matters worse, all the wealth is concentrated on a handful of people in the world's richest countries.",
                "level_image": "https://practiqa-media.s3.amazonaws.com/media/media/2021/05/25/help.jfif",
                "level_stage": 2,
                "level_helper_id": None,
                "level_background": {
                    "colors": [
                        "#F9E285",
                        "#6FCEC0"
                    ],
                    "vector": "90"
                },
                'level_events': {
                    "event_title": "Event 6",
                    "event_name": "Event 6",
                    "event_description": "Text6",
                    "event_image": "https://practiqa-media.s3.amazonaws.com/media/media/2021/05/25/help.jfif",
                    "event_stage": 6,
                    "event_background": {
                        "colors": [
                            "#F9E285",
                            "#6FCEC0"
                        ],
                        "vector": "90"
                    },
                    "event_helper_id": None,
                    "is_completed": False
                }
            }
        }


class NotificationLevel(BaseModel):
    data: List[Level]
    

class NotificationAchievement(BaseModel):
    data: SchemaAchievment
    
