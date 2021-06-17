from fastapi import APIRouter

hobby = APIRouter(prefix='/hobby', tags=['Hobby Crud'])


from . import hobbys
from . import reflections
