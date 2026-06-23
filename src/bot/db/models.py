from sqlalchemy import Column, BigInteger, Integer, DateTime, func, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    telegram_id = Column(BigInteger, primary_key=True, index=True)
    coins = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    last_daily = Column(DateTime(timezone=True), nullable=True)
    boosts_available = Column(Integer, default=0)
    wallet_address = Column(String(100), nullable=True)        # ארנק USDT של המשתמש
    role = Column(String(20), default="user")                  # user, verified, admin, founder
    is_kyc = Column(Boolean, default=False)
    referrer_id = Column(BigInteger, nullable=True)  # who referred this user                    # KYC מאומת
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, index=True)
    item = Column(String(50))
    amount_usdt = Column(Integer)                              # סכום ב-USDT (cents)
    tx_hash = Column(String(100), nullable=True)               # hash של עסקת TON
    status = Column(String(20), default="pending")             # pending, confirmed, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class GroupInfo(Base):`n    __tablename__ = "groups"`n`n    id = Column(BigInteger, primary_key=True, index=True)  # chat_id`n    title = Column(String(200))`n    type = Column(String(20))  # group, supergroup`n    added_at = Column(DateTime(timezone=True), server_default=func.now())`n`n`nclass SystemConfig(Base):
    __tablename__ = "system_config"

    key = Column(String(50), primary_key=True)
    value = Column(String(500))


