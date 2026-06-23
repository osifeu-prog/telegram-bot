from datetime import datetime, timezone
from aiogram import Router, types
from aiogram.filters import Command

router = Router()
ADMIN_ID = 8789977826
active_votes = {}

def is_admin(msg: types.Message) -> bool:
    return msg.from_user.id == ADMIN_ID

@router.message(Command("vote_create"))
async def vote_create_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        await message.answer("Usage: /vote_create <question>")
        return
    question = parts[1]
    vote_id = str(len(active_votes) + 1)
    active_votes[vote_id] = {
        "question": question,
        "yes": 0,
        "no": 0,
        "voters": set(),
        "created_at": datetime.now(timezone.utc)
    }
    await message.answer(f"✅ Vote created: #{vote_id}  {question}\nUse /vote to participate.")

@router.message(Command("vote"))
async def vote_cmd(message: types.Message):
    await message.answer("🗳 Active votes coming soon! Check back later.")

@router.message(Command("vote_close"))
async def vote_close_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Usage: /vote_close <vote_id>")
        return
    vote_id = parts[1]
    if vote_id not in active_votes:
        await message.answer("Vote not found.")
        return
    v = active_votes.pop(vote_id)
    await message.answer(f"✅ Vote #{vote_id} closed.\n{v['question']}\n👍 Yes: {v['yes']} | 👎 No: {v['no']}")

@router.message(Command("vote_stats"))
async def vote_stats_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    if not active_votes:
        await message.answer("No active votes.")
        return
    lines = ["📊 Active Votes:"]
    for vid, v in active_votes.items():
        lines.append(f"#{vid}: {v['question']} (👍{v['yes']} 👎{v['no']})")
    await message.answer("\n".join(lines))

