from typing import Optional, Union
from pydantic import BaseModel, UUID4


class SchemaMessage(BaseModel):
    message: str


class SchemaMessageCreate(BaseModel):
    id: int = 0
    message: str = 'successfully created'


class SchemaMessageDelete(BaseModel):
    id: Optional[Union[int, UUID4]]
    message: str = 'deleted successfully'


class SchemaMessageUpdate(BaseModel):
    id: Optional[int]
    message: str = 'successfully updated'


class NotificationCreate(BaseModel):
    data: SchemaMessageCreate
    


class NotificationDelete(BaseModel):
    data: SchemaMessageDelete
    


class NotificationUpdate(BaseModel):
    data: SchemaMessageUpdate
    
