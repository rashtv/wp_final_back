from pydantic import BaseModel


class User(BaseModel):
    id: int
    firstname: str
    surname: str
    username: str
    password: str
    phone_number: str
    profile_photo: str
    bonus_balance: float

    class Config:
        from_attributes = True
