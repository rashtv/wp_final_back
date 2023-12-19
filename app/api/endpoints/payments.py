from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.crud.payments import (
    create_payment,
    get_payment,
    get_all_payments,
    update_payment,
    delete_payment, get_all_payments_by_user_id
)

from app.database import get_db

from app.models.payments import Payment

router = APIRouter()


@router.post("/", response_model=Payment)
def create_payment_endpoint(payment: Payment, db: Session = Depends(get_db)):
    payment = create_payment(db, payment)
    if payment is None:
        raise HTTPException(status_code=400)
    return payment


@router.get("/{payment_id}", response_model=Payment)
def read_payment_endpoint(payment_id: int, db: Session = Depends(get_db)):
    db_payment = get_payment(db, payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment


@router.get("/", response_model=list[Payment])
def read_all_payments_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_payments(db, skip=skip, limit=limit)


@router.get("/by_user_id/{user_id}", response_model=list[Payment])
def read_all_payments_by_user_id_endpoint(user_id: int, db: Session = Depends(get_db)):
    return get_all_payments_by_user_id(db, user_id)


@router.put("/{payment_id}", response_model=Payment)
def update_payment_endpoint(
        payment_id: int,
        new_payment_data: dict,
        db: Session = Depends(get_db)
):
    db_payment = update_payment(db, payment_id, new_payment_data)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment


@router.delete("/{payment_id}", response_model=Payment)
def delete_payment_endpoint(payment_id: int, db: Session = Depends(get_db)):
    db_payment = delete_payment(db, payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment
