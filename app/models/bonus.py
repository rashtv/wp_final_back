from datetime import datetime

from pydantic import BaseModel


class Bonus(BaseModel):
    user_id: int
    amount: float
    date: datetime

    class Config:
        from_attributes = True
