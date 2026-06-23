from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, Text, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    telegram_id = Column(BigInteger, primary_key=True, index=True)
    coins = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    last_daily = Column(DateTime(timezone=True), nullable=True)
    boosts_available = Column(Integer, default=0)
    wallet_address = Column(String(100), nullable=True)
    role = Column(String(20), default="user")
    is_kyc = Column(Boolean, default=False)
    referrer_id = Column(BigInteger, nullable=True)
    language = Column(String(5), default='en')
    notifications_enabled = Column(Boolean, default=True)
    achievements = Column(Text, default="[]")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, index=True)
    item = Column(String(50))
    amount_usdt = Column(Integer)
    tx_hash = Column(String(100), nullable=True)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class GroupInfo(Base):
    __tablename__ = "groups"
    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(200))
    type = Column(String(20))
    added_at = Column(DateTime(timezone=True), server_default=func.now())


class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String(500))
    options = Column(Text)  # JSON list of options
    created_by = Column(BigInteger)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    closes_at = Column(DateTime(timezone=True), nullable=True)

class SystemConfig(Base):
    __tablename__ = "system_config"
    key = Column(String(50), primary_key=True)
    value = Column(String(500))




