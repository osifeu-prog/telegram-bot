from sqlalchemy import Column, BigInteger, Integer, DateTime, func, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    telegram_id = Column(BigInteger, primary_key=True, index=True)
    coins = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    last_daily = Column(DateTime(timezone=True), nullable=True)
    boosts_available = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, index=True)
    item = Column(String(50))
    amount_stars = Column(Integer)
    payload = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
