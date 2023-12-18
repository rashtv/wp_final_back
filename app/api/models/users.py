from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base

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
