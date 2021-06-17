from pydantic import BaseModel
from typing import Optional
import datetime


class FSM_APP(BaseModel):
    count_user_hobby: int
    current_hobby_id: int
    start_day: datetime.date
    current_day: Optional[datetime.date]
    last_day: Optional[datetime.date]
    in_a_row_day_open_app: int
    max_row_day_open_app: int
    last_day_doing_reflection_day: Optional[datetime.date]
    in_a_row_day_doing_reflection_day: int
    current_level: int
    no_active_in_a_row_day: int
    no_active_in_a_row_day_reflection_day: int
    progress_level: int
    event_key: int
    next_day_is_day_off: Optional[datetime.date]
    
    
class FSM_Hobby(BaseModel):
    hobby_last_day: datetime.date
    last_day_doing_routine: Optional[datetime.date]
    last_day_doing_reflection_routine: Optional[datetime.date]
    in_a_row_day_doing_routine: int
    in_a_row_day_doing_reflection_routine: int
    no_active_in_a_row_day_doing_routine: int
    no_active_in_a_row_day_doing_reflection_routine: int
