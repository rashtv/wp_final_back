from pydantic import BaseModel


class Subcategory(BaseModel):
    id: int
    category_id: int
    title: str

    class Config:
        from_attributes = True
