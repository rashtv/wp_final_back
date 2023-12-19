from datetime import datetime

from pydantic import BaseModel


class BankAccount(BaseModel):
    user_id: int
    balance: float
    account_type: str
    card_number: str
    opening_date: datetime

    class Config:
        from_attributes = True
