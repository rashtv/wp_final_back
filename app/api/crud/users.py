from sqlalchemy.orm import Session
from app.database import User


def create_user(db: Session, user: User):
    u = User(
        id=user.id,
        firstname=user.firstname,
        surname=user.surname,
        username=user.username,
        password=user.password,
        phone_number=user.phone_number,
        profile_photo=user.profile_photo,
        bonus_balance=user.bonus_balance,
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, new_user_data: dict):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        for key, value in new_user_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
