from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.crud.bank_accounts import (
    create_bank_account, get_bank_account, get_bank_account_by_card_number, get_all_bank_accounts, update_bank_account,
    delete_bank_account
)
from app.models.bank_accounts import BankAccount

router = APIRouter()


@router.post("/", response_model=BankAccount)
def create_bank_account_endpoint(bank_account: BankAccount, db: Session = Depends(get_db)):
    return create_bank_account(db, bank_account)


@router.get("/{bank_account_id}", response_model=BankAccount)
def read_bank_account_endpoint(bank_account_id: int, db: Session = Depends(get_db)):
    db_bank_account = get_bank_account(db, bank_account_id)
    if db_bank_account is None:
        raise HTTPException(status_code=404, detail="Bank account not found")
    return db_bank_account


@router.get("/by_card_number/{card_number}", response_model=BankAccount)
def read_bank_account_by_card_number_endpoint(card_number: str, db: Session = Depends(get_db)):
    db_bank_account = get_bank_account_by_card_number(db, card_number)
    if db_bank_account is None:
        raise HTTPException(status_code=404, detail="Bank account not found")
    return db_bank_account


@router.get("/", response_model=list[BankAccount])
def read_all_bank_accounts_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_bank_accounts(db, skip=skip, limit=limit)


@router.put("/{bank_account_id}", response_model=BankAccount)
def update_bank_account_endpoint(
        bank_account_id: int,
        new_bank_account_data: dict,
        db: Session = Depends(get_db)
):
    db_bank_account = update_bank_account(db, bank_account_id, new_bank_account_data)
    if db_bank_account is None:
        raise HTTPException(status_code=404, detail="Bank account not found")
    return db_bank_account


@router.delete("/{bank_account_id}", response_model=BankAccount)
def delete_bank_account_endpoint(bank_account_id: int, db: Session = Depends(get_db)):
    db_bank_account = delete_bank_account(db, bank_account_id)
    if db_bank_account is None:
        raise HTTPException(status_code=404, detail="Bank account not found")
    return db_bank_account
