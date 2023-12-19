import datetime

from sqlalchemy.orm import Session
from app.database import Bonus


def create_bonus(db: Session, bonus: Bonus):
    b = Bonus(
        id=bonus.id,
        user_id=bonus.user_id,
        amount=bonus.amount,
        date=bonus.date,
    )
    db.add(b)
    db.commit()
    db.refresh(b)
    return bonus


def get_bonus(db: Session, bonus_id: int):
    return db.query(Bonus).filter(Bonus.id == bonus_id).first()


def get_all_bonuses(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Bonus).offset(skip).limit(limit).all()


def get_all_bonuses_by_user_id(db: Session, user_id: int):
    return db.query(Bonus).filter(Bonus.user_id == user_id).all()


def update_bonus(db: Session, bonus_id: int, new_transaction_data: dict):
    db_bonus = db.query(Bonus).filter(Bonus.id == bonus_id).first()
    if db_bonus:
        for key, value in new_transaction_data.items():
            if key == "date":
                value = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
            setattr(db_bonus, key, value)
        db.commit()
        db.refresh(db_bonus)
    return db_bonus


def delete_bonus(db: Session, bonus_id: int):
    db_bonus = db.query(Bonus).filter(Bonus.id == bonus_id).first()
    if db_bonus:
        db.delete(db_bonus)
        db.commit()
    return db_bonus
