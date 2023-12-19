from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from app.api.crud.users import (
    get_user_by_username,
    get_all_users,
    update_user,
    delete_user, get_user,
)
from app.database import get_db, Token, User as dbUser
from app.models.users import User

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer is responsible for extracting and verifying the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "aleeex"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Retrieve user based on token
    print(token)
    user = db.query(dbUser).join(Token).filter(Token.token == token).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return user


# Create a new user (sign up)
@router.post("/signup/", response_model=User)
def create_user(user: User, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    user = dbUser(
        firstname=user.firstname,
        surname=user.surname,
        username=user.username,
        password=hashed_password,
        phone_number=user.phone_number,
        profile_photo=user.profile_photo,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Authenticate user and return access token (sign in)
@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(dbUser).filter(dbUser.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    # Save token in the database
    token = Token(token=access_token, user_id=user.id)
    db.add(token)
    db.commit()

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/{user_id}", response_model=User)
def read_user_by_id_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/by_username/{username}", response_model=dict)
def read_user_id_by_username_endpoint(
        username: str,
        db: Session = Depends(get_db)
):
    db_user = get_user_by_username(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": db_user.id}


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
