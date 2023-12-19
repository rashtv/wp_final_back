from sqlalchemy.orm import Session
from app.database import Transaction, BankAccount


def create_transaction(db: Session, transaction: Transaction):
    print(transaction)
    sender_acc = db.query(BankAccount).filter(BankAccount.user_id == transaction.user_id).first()
    receiver_acc = db.query(BankAccount).filter(BankAccount.user_id == transaction.receiver_account_id).first()
    if sender_acc is None or receiver_acc is None:
        return None
    if sender_acc.balance < transaction.amount:
        return None
    t = Transaction(
        user_id=transaction.user_id,
        sender_account_id=transaction.sender_account_id,
        receiver_account_id=transaction.receiver_account_id,
        amount=transaction.amount,
        date=transaction.date,
        transaction_type=transaction.transaction_type
    )
    sender_acc.balance = sender_acc.balance - transaction.amount
    receiver_acc.balance += transaction.amount
    db.add(sender_acc)
    db.add(receiver_acc)
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
