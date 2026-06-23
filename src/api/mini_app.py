from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from datetime import datetime, timedelta
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User
from src.bot.bot import bot

router = APIRouter()

class ClaimRequest(BaseModel):
    telegram_id: int

@router.get("/api/user/{telegram_id}")
async def get_user(telegram_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if not user:
            return {"coins": 0, "streak": 0, "can_claim": True}
        can_claim = not user.last_daily or (datetime.utcnow() - user.last_daily) >= timedelta(hours=24)
        return {"coins": user.coins, "streak": user.current_streak, "can_claim": can_claim}

@router.post("/api/daily/claim")
async def claim_daily(req: ClaimRequest):
    now = datetime.utcnow()
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == req.telegram_id))
        user = result.scalar_one_or_none()
        if not user:
            user = User(telegram_id=req.telegram_id, coins=0, current_streak=0)
            session.add(user)
            await session.commit()
        if user.last_daily and (now - user.last_daily) < timedelta(hours=24):
            raise HTTPException(status_code=400, detail="Already claimed today")
        if user.last_daily and (now - user.last_daily) < timedelta(hours=48):
            user.current_streak += 1
        else:
            user.current_streak = 1
        streak_bonus = min(user.current_streak * 2, 40)
        reward = 10 + streak_bonus
        user.coins += reward
        user.last_daily = now
        await session.commit()
        return {"coins": user.coins, "streak": user.current_streak, "reward": reward}

class BuyRequest(BaseModel):
    telegram_id: int
    item: str

@router.post("/api/store/buy")
async def buy_item(req: BuyRequest):
    if req.item == 'boost':
        prices = [{"label": "Streak Boost", "amount": 100}]
        invoice_link = await bot.create_invoice_link(
            title="Streak Boost",
            description="Protect your streak if you miss a day",
            payload="boost_purchase",
            currency="XTR",
            prices=prices,
        )
        return {"invoice_url": invoice_link}
    else:
        raise HTTPException(status_code=400, detail="Unknown item")
