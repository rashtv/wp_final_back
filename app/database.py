import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "sqlite:///jusan.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, index=True)
    surname = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    phone_number = Column(String, unique=True, index=True)
    profile_photo = Column(String)
    bonus_balance = Column(Float)


class BankAccount(Base):
    __tablename__ = "bank_accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey(User.id), unique=True, index=True)
    balance = Column(Float)
    account_type = Column(String, index=True)
    card_number = Column(String, unique=True, index=True)
    opening_date = Column(DateTime, index=True, default=datetime.datetime.now(), info={"read_only": True})
