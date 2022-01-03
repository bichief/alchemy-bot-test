from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKeyConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from sqlalchemy.orm import relationship

from data.config import engine

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    telegram_id = Column(BigInteger(), nullable=False, unique=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    state = Column(String(), default='false')

    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now)

    registration = relationship('Registration')

class Registration(Base):
    __tablename__ = 'registration'
    id = Column(Integer, primary_key=True)
    users_id = Column(Integer(), ForeignKey('users.id'), unique=True)
    phone = Column(String(15), nullable=False)
    email = Column(String(200), nullable=False)


Base.metadata.create_all(engine)
