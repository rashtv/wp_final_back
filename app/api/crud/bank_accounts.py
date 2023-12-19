import datetime

from sqlalchemy.orm import Session
from app.database import BankAccount


def create_bank_account(db: Session, bank_account: BankAccount):
    ba = BankAccount(
        id=bank_account.id,
        user_id=bank_account.user_id,
        balance=bank_account.balance,
        account_type=bank_account.account_type,
        card_number=bank_account.card_number,
        opening_date=bank_account.opening_date,
    )
    db.add(ba)
    db.commit()
    db.refresh(ba)
    return bank_account


def get_bank_account(db: Session, bank_account_id: int):
    return db.query(BankAccount).filter(BankAccount.id == bank_account_id).first()


def get_bank_account_by_user_id(db: Session, user_id: int):
    return db.query(BankAccount).filter(BankAccount.user_id == user_id).first()


def get_bank_account_by_card_number(db: Session, card_number: str):
    return db.query(BankAccount).filter(BankAccount.card_number == card_number).first()


def get_all_bank_accounts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(BankAccount).offset(skip).limit(limit).all()


def update_bank_account(db: Session, bank_account_id: int, new_bank_account_data: dict):
    db_bank_account = db.query(BankAccount).filter(BankAccount.id == bank_account_id).first()
    if db_bank_account:
        for key, value in new_bank_account_data.items():
            if key == "opening_date":
                value = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
            setattr(db_bank_account, key, value)
        db.commit()
        db.refresh(db_bank_account)
    return db_bank_account


def delete_bank_account(db: Session, bank_account_id: int):
    db_bank_account = db.query(BankAccount).filter(BankAccount.id == bank_account_id).first()
    if db_bank_account:
        db.delete(db_bank_account)
        db.commit()
    return db_bank_account
