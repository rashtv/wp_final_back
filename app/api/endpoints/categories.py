from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.crud.categories import (
    create_category,
    get_category,
    get_all_categories,
    update_category,
    delete_category
)
from app.database import get_db

from app.models.categories import Category

router = APIRouter()


@router.post("/", response_model=Category)
def create_category_endpoint(category: Category, db: Session = Depends(get_db)):
    return create_category(db, category)


@router.get("/{category_id}", response_model=Category)
def read_category_endpoint(category_id: int, db: Session = Depends(get_db)):
    db_category = get_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.get("/", response_model=list[Category])
def read_all_categories_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_categories(db, skip=skip, limit=limit)


@router.put("/{category_id}", response_model=Category)
def update_category_endpoint(
        category_id: int,
        new_category_data: dict,
        db: Session = Depends(get_db)
):
    db_category = update_category(db, category_id, new_category_data)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.delete("/{category_id}", response_model=Category)
def delete_category_endpoint(category_id: int, db: Session = Depends(get_db)):
    db_category = delete_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category
