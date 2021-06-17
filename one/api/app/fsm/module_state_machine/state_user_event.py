from fastapi.logger import logger
from typing import Dict, Iterator, NoReturn, Tuple
from databases.backends.postgres import Record

from app.crud import crud_user, crud_level
from app.fsm import crud_fsm

class EventStateMachine:
    

    async def get_level_event(self) -> Iterator[Record]:
        return await crud_level.get_current_level_event(self.user_id, self.app.current_level)

    async def get_bonus_event(self) -> int:
        return await crud_level.get_current_level_event(self.user_id, 99)

    async def _get_state_moderate(self) -> Iterator[Record]:
        return await crud_user.history.get_state_reflection_hobby(
            self.user_id, self.user_hobby_id, self.day)

    async def save_event_to_completed(self, event_id: int) -> NoReturn:
        if not self.user_hobby_id:
            logger.warning("NOT USER HOBBY TO SAVE EVENT COMLETED")

            self.user_hobby_id = await crud_fsm.get_last_hobby_id(self.user_id)
        await crud_level.close_level_event(self.user_id, event_id, self.user_hobby_id)

    async def delete_event_id(self, event_id: int) -> NoReturn:
        await crud_fsm.delete_last_event_key(self.user_id, event_id)

    async def add_event_id(self, event_id: int) -> NoReturn:
        await crud_fsm.add_last_event_key(self.user_id, event_id)

    async def all_last_event_id(self) -> Iterator[Record]:
        return await crud_fsm.all_last_event_key(self.user_id)

