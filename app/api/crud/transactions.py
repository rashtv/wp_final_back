import datetime

from sqlalchemy.orm import Session
from app.database import Transaction


def create_transaction(db: Session, transaction: Transaction):
    t = Transaction(
        user_id=transaction.user_id,
        sender_account_id=transaction.sender_account_id,
        receiver_account_id=transaction.receiver_account_id,
        amount=transaction.amount,
        date=transaction.date,
        transaction_type=transaction.transaction_type
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return transaction


def get_transaction(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()


def get_all_transactions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Transaction).offset(skip).limit(limit).all()


def get_all_transactions_by_user_id(db: Session, user_id: int):
    return db.query(Transaction).filter(Transaction.user_id == user_id).all()


def update_transaction(db: Session, transaction_id: int, new_transaction_data: dict):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction:
        for key, value in new_transaction_data.items():
            if key == "date":
                value = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
            setattr(db_transaction, key, value)
        db.commit()
        db.refresh(db_transaction)
    return db_transaction


def delete_transaction(db: Session, transaction_id: int):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
    return db_transaction
