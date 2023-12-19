from datetime import datetime

from pydantic import BaseModel


class Loan(BaseModel):
    user_id: int
    amount: float
    status: str
    start_date: datetime
    end_date: datetime

    class Config:
        from_attributes = True
