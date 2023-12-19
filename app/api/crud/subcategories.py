import datetime

from sqlalchemy.orm import Session
from app.database import Subcategory


def create_subcategory(db: Session, subcategory: Subcategory):
    s = Subcategory(
        id=subcategory.id,
        category_id=subcategory.category_id,
        title=subcategory.title,
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return subcategory


def get_subcategory(db: Session, subcategory_id: int):
    return db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()


def get_all_subcategories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Subcategory).offset(skip).limit(limit).all()


def get_all_subcategories_by_category_id(db: Session, category_id: int):
    return db.query(Subcategory).filter(Subcategory.category_id == category_id).all()


def update_subcategory(db: Session, subcategory_id: int, new_subcategory_data: dict):
    db_subcategory = db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()
    if db_subcategory:
        for key, value in new_subcategory_data.items():
            setattr(db_subcategory, key, value)
        db.commit()
        db.refresh(db_subcategory)
    return db_subcategory


def delete_subcategory(db: Session, subcategory_id: int):
    db_subcategory = db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()
    if db_subcategory:
        db.delete(db_subcategory)
        db.commit()
    return db_subcategory
