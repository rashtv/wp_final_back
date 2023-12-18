from datetime import datetime

from pydantic import BaseModel


class Transaction(BaseModel):
    id: int
    user_id: int
    sender_account_id: int
    receiver_account_id: int
    amount: float
    date: datetime
    transaction_type: str

    class Config:
        from_attributes = True
