from pydantic import BaseModel


class Medicine(BaseModel):
    name: str
    frequency: int
    duration: int
    user_id: int

class GetSchedule(BaseModel):
    user_id: int
    id: int

class GetSchedules(BaseModel):
    user_id: int