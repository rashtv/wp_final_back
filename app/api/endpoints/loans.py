from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.crud.loans import create_loan, get_loan, get_all_loans, update_loan, delete_loan, get_all_loans_by_user_id
from app.database import get_db

from app.models.loans import Loan

router = APIRouter()


@router.post("/", response_model=Loan)
def create_loan_endpoint(loan: Loan, db: Session = Depends(get_db)):
    return create_loan(db, loan)


@router.get("/{loan_id}", response_model=Loan)
def read_loan_endpoint(loan_id: int, db: Session = Depends(get_db)):
    db_loan = get_loan(db, loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db_loan


@router.get("/", response_model=list[Loan])
def read_all_loans_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_loans(db, skip=skip, limit=limit)


@router.get("/by_user_id/{user_id}", response_model=list[Loan])
def read_all_loans_by_user_id_endpoint(user_id: int, db: Session = Depends(get_db)):
    return get_all_loans_by_user_id(db, user_id)


@router.put("/{loan_id}", response_model=Loan)
def update_loan_endpoint(
        loan_id: int,
        new_loan_data: dict,
        db: Session = Depends(get_db)
):
    db_loan = update_loan(db, loan_id, new_loan_data)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db_loan


@router.delete("/{loan_id}", response_model=Loan)
def delete_loan_endpoint(loan_id: int, db: Session = Depends(get_db)):
    db_loan = delete_loan(db, loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db_loan
