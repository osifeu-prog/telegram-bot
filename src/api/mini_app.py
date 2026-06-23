import json
from fastapi import APIRouter, Query
from sqlalchemy import select
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User, Vote

router = APIRouter()

@router.get("/api/votes")
async def get_votes():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Vote).where(Vote.is_active == True)
        )
        votes = result.scalars().all()
    return [
        {"id": v.id, "question": v.question, "options": json.loads(v.options)}
        for v in votes
    ]

@router.post("/api/vote/{vote_id}/{option_index}")
async def cast_vote(vote_id: int, option_index: int):
    async with AsyncSessionLocal() as session:
        vote = await session.get(Vote, vote_id)
        if not vote:
            return {"error": "Vote not found"}
        options = json.loads(vote.options)
        if 0 <= option_index < len(options):
            # In real app, store vote record; here we just return success
            return {"status": "ok", "chosen": options[option_index]}
        return {"error": "Invalid option"}
@router.post("/api/set_path")
async def set_path(data: dict):
    telegram_id = data.get("telegram_id")
    path = data.get("path")
    if not telegram_id or path not in ("gaming", "community"):
        return {"error": "Invalid data"}
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if not user:
            user = User(telegram_id=telegram_id, coins=50, role=path)
            session.add(user)
        else:
            user.role = path
            user.coins += 50
        await session.commit()
    return {"status": "ok", "coins": user.coins}

@router.get("/api/user/{user_id}")
async def get_user(user_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == user_id))
        user = result.scalar_one_or_none()
    if not user:
        return {"error": "User not found"}
    return {
        "telegram_id": user.telegram_id,
        "coins": user.coins,
        "current_streak": user.current_streak,
        "last_daily": user.last_daily.isoformat() if user.last_daily else None
    }

@router.get("/api/top")
async def get_top(limit: int = Query(default=10, le=50)):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User.telegram_id, User.coins, User.current_streak)
            .order_by(User.coins.desc())
            .limit(limit)
        )
        rows = result.all()
    return [
        {"rank": i+1, "telegram_id": tid, "coins": coins, "streak": streak}
        for i, (tid, coins, streak) in enumerate(rows)
    ]


