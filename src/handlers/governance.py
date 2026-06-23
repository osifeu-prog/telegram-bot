from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select, func
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import Vote, User
import json

router = Router()

ADMIN_ID = 8789977826  # fallback

def is_admin(msg: types.Message) -> bool:
    return msg.from_user.id == ADMIN_ID

@router.message(Command("propose"))
async def propose_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    # Usage: /propose <question> | <option1>,<option2>,...
    text = message.text.removeprefix("/propose ").strip()
    if not text or '|' not in text:
        await message.answer("Usage: /propose <question> | <option1>,<option2>,...")
        return
    parts = text.split('|', 1)
    question = parts[0].strip()
    options = [o.strip() for o in parts[1].split(',') if o.strip()]
    if len(options) < 2:
        await message.answer("Need at least 2 options.")
        return
    async with AsyncSessionLocal() as session:
        vote = Vote(
            question=question,
            options=json.dumps(options),
            created_by=message.from_user.id
        )
        session.add(vote)
        await session.commit()
    await message.answer(f"✅ Vote created! ID: {vote.id}\nQuestion: {question}")

@router.message(Command("vote"))
async def vote_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Vote).where(Vote.is_active == True)
        )
        votes = result.scalars().all()
    if not votes:
        await message.answer("No active votes.")
        return
    lines = ["🗳 **Active Votes**"]
    for v in votes:
        lines.append(f"/vote_{v.id}  {v.question}")
    await message.answer("\n".join(lines))

# Dynamic handlers for each vote
@router.message(Command(prefix="vote_"))
async def vote_detail(message: types.Message):
    vote_id = int(message.text.split('_')[1])
    async with AsyncSessionLocal() as session:
        vote = await session.get(Vote, vote_id)
    if not vote:
        await message.answer("Vote not found.")
        return
    options = json.loads(vote.options)
    text = f"**{vote.question}**\n\nOptions:"
    for i, opt in enumerate(options, 1):
        text += f"\n{i}. {opt}"
    text += "\n\nReply with the option number to vote."
    await message.answer(text)

# Listen for plain numbers (1,2,...) as votes (simplified)
@router.message()
async def handle_vote(message: types.Message):
    # Only process if the user is replying to a vote (not a command)
    if not message.text or not message.text.strip().isdigit():
        return
    option_num = int(message.text.strip())
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Vote).where(Vote.is_active == True).order_by(Vote.id.desc())
        )
        active_votes = result.scalars().all()
        if not active_votes:
            return
        # Assume the latest active vote is the one the user is voting on
        vote = active_votes[0]
        options = json.loads(vote.options)
        if 1 <= option_num <= len(options):
            chosen = options[option_num-1]
            await message.answer(f"✅ You voted for: {chosen} in vote #{vote.id}")
            # (in production, store the vote in a separate table to prevent duplicates)
        else:
            await message.answer("Invalid option number.")

@router.message(Command("governance"))
async def governance_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Vote).order_by(Vote.id.desc()).limit(10)
        )
        votes = result.scalars().all()
    if not votes:
        await message.answer("No votes yet.")
        return
    lines = ["🏛 **Governance Dashboard**"]
    for v in votes:
        status = "🟢 Open" if v.is_active else "🔴 Closed"
        lines.append(f"#{v.id} [{status}] {v.question}")
    await message.answer("\n".join(lines))
