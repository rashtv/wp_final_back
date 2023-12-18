import datetime

from sqlalchemy.orm import Session
from app.database import Loan


def create_loan(db: Session, loan: Loan):
    lo = Loan(
        id=loan.id,
        user_id=loan.user_id,
        amount=loan.amount,
        status=loan.status,
        start_date=loan.start_date,
        end_date=loan.end_date
    )
    db.add(lo)
    db.commit()
    db.refresh(lo)
    return loan


def get_loan(db: Session, loan_id: int):
    return db.query(Loan).filter(Loan.id == loan_id).first()


def get_all_loans(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Loan).offset(skip).limit(limit).all()


def update_loan(db: Session, loan_id: int, new_loan_data: dict):
    db_loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if db_loan:
        for key, value in new_loan_data.items():
            if key == "start_date" or key == "end_date":
                value = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
            setattr(db_loan, key, value)
        db.commit()
        db.refresh(db_loan)
    return db_loan


def delete_loan(db: Session, loan_id: int):
    db_loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if db_loan:
        db.delete(db_loan)
        db.commit()
    return db_loan
