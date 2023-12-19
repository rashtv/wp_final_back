from pydantic import BaseModel


class User(BaseModel):
    firstname: str
    surname: str
    username: str
    password: str
    phone_number: str
    profile_photo: str

    class Config:
        from_attributes = True
