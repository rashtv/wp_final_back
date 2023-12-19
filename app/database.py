import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Boolean
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
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String, index=True)
    surname = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    phone_number = Column(String, unique=True, index=True)
    profile_photo = Column(String)
    bonus_balance = Column(Float, default=0)


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))


class BankAccount(Base):
    __tablename__ = "bank_accounts"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(ForeignKey(User.id), unique=True, index=True)
    balance = Column(Float)
    account_type = Column(String, index=True)
    card_number = Column(String, unique=True, index=True)
    opening_date = Column(DateTime, index=True, default=datetime.datetime.now(), info={"read_only": True})


class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(ForeignKey(User.id), unique=False, index=True)
    amount = Column(Float)
    status = Column(String, index=True)
    start_date = Column(DateTime, index=True, default=datetime.datetime.now())
    end_date = Column(DateTime, index=True)


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(ForeignKey(User.id), index=True)
    sender_account_id = Column(ForeignKey(BankAccount.id), unique=False, index=True)
    receiver_account_id = Column(ForeignKey(BankAccount.id), unique=False, index=True)
    amount = Column(Float)
    date = Column(DateTime, index=True)
    transaction_type = Column(String, index=True)


class Bonus(Base):
    __tablename__ = "bonuses"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(ForeignKey(User.id), unique=False, index=True)
    amount = Column(Float)
    date = Column(DateTime, index=True)


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)


class Subcategory(Base):
    __tablename__ = "subcategories"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_id = Column(ForeignKey(Category.id), unique=False, index=True)
    title = Column(String)


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(ForeignKey(User.id), index=True)
    category_id = Column(ForeignKey(Category.id), index=True)
    subcategory_id = Column(ForeignKey(Subcategory.id), index=True)
    amount = Column(Float)
    date = Column(DateTime, index=True)
