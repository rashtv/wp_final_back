import datetime

from sqlalchemy.orm import Session
from app.database import Category


def create_category(db: Session, category: Category):
    c = Category(
        id=category.id,
        title=category.title,
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return category


def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def get_all_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Category).offset(skip).limit(limit).all()


def update_category(db: Session, category_id: int, new_category_data: dict):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        for key, value in new_category_data.items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category
