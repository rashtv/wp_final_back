from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.crud.subcategories import (
    create_subcategory, get_subcategory, get_all_subcategories, update_subcategory, delete_subcategory
)
from app.database import get_db

from app.models.subcategories import Subcategory

router = APIRouter()


@router.post("/", response_model=Subcategory)
def create_subcategory_endpoint(subcategory: Subcategory, db: Session = Depends(get_db)):
    return create_subcategory(db, subcategory)


@router.get("/{subcategory_id}", response_model=Subcategory)
def read_subcategory_endpoint(subcategory_id: int, db: Session = Depends(get_db)):
    db_subcategory = get_subcategory(db, subcategory_id)
    if db_subcategory is None:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    return db_subcategory


@router.get("/", response_model=list[Subcategory])
def read_all_subcategories_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_subcategories(db, skip=skip, limit=limit)


@router.put("/{subcategory_id}", response_model=Subcategory)
def update_subcategory_endpoint(
        subcategory_id: int,
        new_subcategory_data: dict,
        db: Session = Depends(get_db)
):
    db_subcategory = update_subcategory(db, subcategory_id, new_subcategory_data)
    if db_subcategory is None:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    return db_subcategory


@router.delete("/{subcategory_id}", response_model=Subcategory)
def delete_subcategory_endpoint(subcategory_id: int, db: Session = Depends(get_db)):
    db_subcategory = delete_subcategory(db, subcategory_id)
    if db_subcategory is None:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    return db_subcategory
