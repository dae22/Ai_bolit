from pydantic import BaseModel


class Medicine(BaseModel):
    name: str
    frequency: str
    duration: int
    user_id: int