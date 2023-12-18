from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.crud.users import (
    create_user,
    get_user,
    get_user_by_username,
    get_all_users,
    update_user,
    delete_user,
)
from app.models.users import User

router = APIRouter()


@router.post("/", response_model=User)
def create_user_endpoint(user: User, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.get("/{user_id}", response_model=User)
def read_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/by_username/{username}", response_model=User)
def read_user_by_username_endpoint(username: str, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/", response_model=list[User])
def read_all_users_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_users(db, skip=skip, limit=limit)


@router.put("/{user_id}", response_model=User)
def update_user_endpoint(user_id: int, new_user_data: dict, db: Session = Depends(get_db)):
    db_user = update_user(db, user_id, new_user_data)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}", response_model=User)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
