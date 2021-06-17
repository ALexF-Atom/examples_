from app.schemas.custom_type import ImageRichField, ColorsListBackground

from pydantic import BaseModel, validator
from typing import List, Dict, Optional, Union, Literal


class SchemaLevelReflection(BaseModel):
    level: int
    title: str
    background_colors: Optional[ColorsListBackground]
    background_vector: Optional[int]
    text_color: Optional[str]
    script: Optional[int] 

    class Config:
        schema_extra = {
            'example': {
                'level': 1,
                'title': 'Very Light',
                'background_colors': ['#74DEEF', '#74DEEF'],
                'background_vector': 180,
                'text_color': '#3F919E',
                'script': '1'
            }
        }

    @validator('script')
    def process_script(cls, value):
        if value is None:
            return 0
        return value


class SchemaLevelTitle(BaseModel):
    image: ImageRichField
    text_header: str
    text_title: str
    text_name: str
    text_color: str
    text_description: str
    text_correlation: Optional[str] = ""
    is_correlation: bool
    desired_time: Optional[int] = 0
    correlation: int
    max_time: Optional[int] = 0
    min_time: Optional[int] = 0


class SchemaReflectionFinal(BaseModel):
    image: ImageRichField
    text: str


class SchemaReflections(BaseModel):
    hobby_id: int 
    text: str 
    complexity: List[SchemaLevelReflection]



class NotificationReflectionFinal(BaseModel):
    data: SchemaReflectionFinal
    
