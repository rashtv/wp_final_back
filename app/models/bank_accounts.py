from datetime import datetime

from pydantic import BaseModel


class BankAccount(BaseModel):
    id: int
    user_id: int
    balance: float
    account_type: str
    card_number: str
    opening_date: datetime

    class Config:
        from_attributes = True
