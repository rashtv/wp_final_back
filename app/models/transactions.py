from pydantic import BaseModel

from models.users import User


class Transaction(BaseModel):
    # TODO

    class Config:
        orm_mode = True
