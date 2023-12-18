from datetime import datetime

from pydantic import BaseModel


class Payment(BaseModel):
    id: int
    user_id: int
    category_id: int
    subcategory_id: int
    amount: float
    date: datetime

    class Config:
        from_attributes = True
