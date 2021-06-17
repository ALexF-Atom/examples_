from app.crud import crud_user
from typing import Iterator
from databases.backends.postgres import Record
from fastapi.logger import logger

from app.fsm.module_event_rules.level_one_event_rules import level_one_rules
from app.fsm import crud_fsm


class EventStateProcessing:
    ...