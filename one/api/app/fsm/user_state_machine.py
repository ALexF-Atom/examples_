from app.schemas.schema_user import user
from typing import Dict
from fastapi.logger import logger
from pydantic import UUID4
from datetime import datetime, timedelta, date

from app.fsm.schema import FSM_APP, FSM_Hobby
from app.fsm import crud_fsm
from app.crud import crud_helper
from .module_state_machine.rule_change_state import RuleChangeState
from .module_state_machine.state_user_event import EventStateMachine


from app.fsm.global_const import ACTION_KEY_900, DAY_OFF, NO_ACTION_KEY, ACTION_ON, RELATED_NAME, RELATION_ACTION_ON_NAME


class UserStateMachine(EventStateMachine, RuleChangeState,):
    def __init__(self, user_id: UUID4, action_key: int,
                 tz_info: int,
                 rel_name_dict: Dict,
                 user_hobby_id: int):
        self.user_id = user_id
        self.tz = tz_info
        self.action_key = int(action_key)
        self.related_key = self.pop_related_data(rel_name_dict)

        self.fulltime = (datetime.utcnow() + timedelta(hours=self.tz))
        self.day = self.fulltime.date()
        self.user_hobby_id = user_hobby_id
        self.app: FSM_APP = None
        self.hobby: FSM_Hobby = None

    @classmethod
    async def init(cls, user_id: UUID4, user_hobby_id: int):
        logger.warning(
            f"START CREATE uid={user_id} user_hobby_id={user_hobby_id}")
        id_app = await crud_fsm.create_state_app(user_id=user_id, current_hobby_id=user_hobby_id)
        id_hobby = await crud_fsm.create_state_routine(user_id=user_id, user_hobby_id=user_hobby_id)
        logger.warning(f"CREATE fsm_app {id_app} fsm_hobby {id_hobby}")
        await crud_fsm.save_action(user_id,
                                   action_key=97,
                                   related_name=RELATED_NAME.get(97, "unknown"),
                                   key_id=int(user_hobby_id))

    @classmethod
    async def compare_and_confirmation_event_completed(cls, user_id: UUID4, event_id: int):
        event_key = await crud_fsm.get_current_event_key(user_id)
        if event_id == event_key:
            user_hobby_id = await crud_fsm.get_current_hobby(user_id)
            # await crud_fsm.closing_level_event(user_id=user_id,
            #                                   event_id=event_id,
            #                                   user_hobby_id=user_hobby_id)
            await crud_fsm.set_current_event_key(user_id=user_id,
                                                 event_id=0)
            return True
        return False

    @classmethod
    async def get_level_info(cls, user_id: UUID4):
        level_info = await crud_fsm.get_state_level_info(user_id=user_id)

        return level_info

    def pop_related_data(self, rel_name_dict):
        key = 0
        name = ""
        if rel_name_dict:
            name, key = rel_name_dict.popitem()
        return int(key)

    def _where_day_off(self, day: date):
        d = DAY_OFF - day.isoweekday()
        if d == 0 or d == 1:
            d = 7
        return day + timedelta(days=d)

    async def logging_(self):
        
        action_key = self.action_key
        key_id = self.related_key
        if self.action_key == 900:
            
            action_key = self.related_key
            key_id = await crud_fsm.get_current_hobby(self.user_id)
            
        elif self.action_key == 212:
            key_id = await crud_helper.get_id_for_mane('custom-timer')
            action_key = 200
        elif self.action_key == 210:
            key_id = await crud_helper.get_id_for_mane('self-reflection')
            action_key = 200
        related_name = RELATED_NAME.get(action_key, "unknown")
        
        await crud_fsm.save_action(
            self.user_id,
            action_key=action_key,
            related_name=related_name,
            key_id=int(key_id))
        
        
    

    async def start(self):
        if self.action_key not in RELATION_ACTION_ON_NAME:
            
            self.user_hobby_id = await crud_fsm.get_current_hobby(self.user_id)
            return self
        
        self.app = FSM_APP.parse_obj(
            await crud_fsm.current_state_app(self.user_id))
        current = self.app.current_hobby_id
        tmp = self.user_hobby_id
        if not tmp:
            tmp = current
        elif tmp != current:
            current = tmp
            await crud_fsm.update_last_hobby(current)
        self.app.current_hobby_id = tmp
        self.user_hobby_id = tmp

        self.hobby = FSM_Hobby.parse_obj(
            await crud_fsm.current_state_routine(self.user_id,
                                                 self.user_hobby_id))
        
        await self.logging_()
        
        await self.change_state()
        
        return self

    async def stop(self):
        if self.action_key not in ACTION_ON:
            return 0
        await crud_fsm.update_state_app(self)
        await crud_fsm.update_state_routine(self)

    async def change_state(self):
        
        if self.action_key == 900 and self.related_key == 100:
            await self.open_app()
        elif self.action_key == 119:
            await self.doing_routine()
        elif self.action_key == 121:
            await self.doing_reflection_hobby()
        elif self.action_key == 123:
            await self.doing_reflection_day()
        if self.action_key == 900:
            await self.process_event_state()


    async def process_event_state(self):
        level_event_ids = await self.get_level_event()
        # bonus_event_ids = await self.get_bonus_event(self.app.current_level)
        
        
        for item in level_event_ids:
            
            if (self.related_key == 102 or self.related_key == 104) and item['stage'] == 4:
                self.app.event_key = item['event_id']
                
                return
            elif self.related_key == 106 and item['stage'] == 7:
                
                self.app.event_key = item['event_id']
                return
            elif self.related_key == 100 and item['stage'] == 1:
                self.app.event_key = item['event_id']
                
                return
        

    async def is_action_completed(self, action_key):
        return await crud_fsm.is_action_in(self.user_id, action_key)


    def __str__(self):
        return f"""
                day =               {self.day}
                start_day =         {self.app.start_day}
                current_day =       {self.app.current_day}
                last_day =          {self.app.last_day}
                open_app =          {self.app.count_open_app}
                open_today =        {self.app.count_open_app_current_day}
                in_row_day =        {self.app.in_a_row_day_open_app}
                in_row_no_active =  {self.app.in_a_row_day_no_active}
                user_hobby_id =     {self.app.current_hobby_id}
                event_key =         {self.event_key}
        """
