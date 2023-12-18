from pydantic import BaseModel


class Category(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True
