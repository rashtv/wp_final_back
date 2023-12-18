from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from app.api.models.users import User

Base = declarative_base()


class BankAccount(Base):
    __tablename__ = "bank_accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey(User.id), unique=True, index=True)
    balance = Column(Float)
    account_type = Column(String, index=True)
    card_number = Column(String, unique=True, index=True)
    opening_date = Column(DateTime, index=True)
