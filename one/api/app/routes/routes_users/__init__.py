from fastapi import APIRouter
from app.schemas.schema_message import SchemaMessage

user = APIRouter(prefix='/user', tags=['User CRUD'],
                 responses={404:{"description": "The item was not found",
                                 "content": {
                                     "application/json": {
                                         "example": {"detail": "Item not found"}
                                     }
                                 }, 
                                 }})

from . import routes_users
from . import routes_properties
from . import routes_history
from . import routes_levels
from . import routes_action
