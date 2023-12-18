from datetime import datetime

from pydantic import BaseModel


class Bonuses(BaseModel):
    id: int
    user_id: int
    amount: float
    date: datetime

    class Config:
        from_attributes = True
