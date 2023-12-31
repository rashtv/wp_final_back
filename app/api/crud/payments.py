import datetime

from sqlalchemy.orm import Session
from app.database import Payment, BankAccount, User


def create_payment(db: Session, payment: Payment, use_bonus: bool = False):
    payer_acc = db.query(BankAccount).filter(BankAccount.user_id == payment.user_id).first()
    payer = db.query(User).filter(User.id == payment.user_id).first()
    to_pay = payment.amount
    from_bonus = 0
    if use_bonus:
        from_bonus = min(to_pay, payer.bonus_balance)
    to_pay -= from_bonus
    print(to_pay, from_bonus)
    if payer_acc is None:
        return None
    if to_pay > payer_acc.balance:
        return None
    payer_acc.balance -= to_pay
    payer.bonus_balance -= from_bonus
    payer.bonus_balance += to_pay / 100
    p = Payment(
        user_id=payment.user_id,
        category_id=payment.category_id,
        subcategory_id=payment.subcategory_id,
        amount=payment.amount,
        date=payment.date,
    )
    db.add(payer_acc)
    db.add(payer)
    db.add(p)
    db.commit()
    db.refresh(p)
    return payment


def get_payment(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.id == payment_id).first()


def get_all_payments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Payment).offset(skip).limit(limit).all()


def get_all_payments_by_user_id(db: Session, user_id: int):
    return db.query(Payment).filter(Payment.user_id == user_id).all()


def update_payment(db: Session, payment_id: int, new_payment_data: dict):
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if db_payment:
        for key, value in new_payment_data.items():
            if key == "date":
                value = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
            setattr(db_payment, key, value)
        db.commit()
        db.refresh(db_payment)
    return db_payment


def delete_payment(db: Session, payment_id: int):
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if db_payment:
        db.delete(db_payment)
        db.commit()
    return db_payment
