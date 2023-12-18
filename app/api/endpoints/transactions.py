from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.crud.transactions import (
    create_transaction,
    get_transaction,
    get_all_transactions,
    update_transaction,
    delete_transaction
)

from app.database import get_db

from app.models.transactions import Transaction

router = APIRouter()


@router.post("/", response_model=Transaction)
def create_transaction_endpoint(transaction: Transaction, db: Session = Depends(get_db)):
    return create_transaction(db, transaction)


@router.get("/{transaction_id}", response_model=Transaction)
def read_transaction_endpoint(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = get_transaction(db, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction


@router.get("/", response_model=list[Transaction])
def read_all_transactions_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_transactions(db, skip=skip, limit=limit)


@router.put("/{transaction_id}", response_model=Transaction)
def update_transaction_endpoint(
        transaction_id: int,
        new_transaction_data: dict,
        db: Session = Depends(get_db)
):
    db_transaction = update_transaction(db, transaction_id, new_transaction_data)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction


@router.delete("/{transaction_id}", response_model=Transaction)
def delete_transaction_endpoint(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = delete_transaction(db, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction