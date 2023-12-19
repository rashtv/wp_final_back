from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.crud.bonuses import (
    create_bonus,
    get_bonus,
    get_all_bonuses,
    update_bonus,
    delete_bonus, get_all_bonuses_by_user_id
)

from app.database import get_db

from app.models.bonus import Bonus

router = APIRouter()


@router.post("/", response_model=Bonus)
def create_bonus_endpoint(bonus: Bonus, db: Session = Depends(get_db)):
    return create_bonus(db, bonus)


@router.get("/{bonus_id}", response_model=Bonus)
def read_bonus_endpoint(bonus_id: int, db: Session = Depends(get_db)):
    db_bonus = get_bonus(db, bonus_id)
    if db_bonus is None:
        raise HTTPException(status_code=404, detail="Bonus not found")
    return db_bonus


@router.get("/", response_model=list[Bonus])
def read_all_bonuses_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_bonuses(db, skip=skip, limit=limit)


@router.get("/by_user_id/{user_id}", response_model=list[Bonus])
def read_all_bonuses_by_user_id_endpoint(user_id: int, db: Session = Depends(get_db)):
    return get_all_bonuses_by_user_id(db, user_id)


@router.put("/{bonus_id}", response_model=Bonus)
def update_bonus_endpoint(
        bonus_id: int,
        new_bonus_data: dict,
        db: Session = Depends(get_db)
):
    db_bonus = update_bonus(db, bonus_id, new_bonus_data)
    if db_bonus is None:
        raise HTTPException(status_code=404, detail="Bonus not found")
    return db_bonus


@router.delete("/{bonus_id}", response_model=Bonus)
def delete_bonus_endpoint(bonus_id: int, db: Session = Depends(get_db)):
    db_bonus = delete_bonus(db, bonus_id)
    if db_bonus is None:
        raise HTTPException(status_code=404, detail="Bonus not found")
    return db_bonus
