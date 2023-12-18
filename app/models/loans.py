from datetime import datetime

from pydantic import BaseModel

from models.users import User


class Loan(BaseModel):
    id: int = 0
    user_id: User.id
    loan_amount: float
    status: str
    start_date: datetime
    end_date: datetime

    class Config:
        orm_mode = True
