from aiogram import Router, types
from aiogram.filters import Command

router = Router()

PROJECT_TASKS = [
    "✅ MVP 100%  daily loop, wallet, shop, mini-app",
    "✅ V1 95%  KYC, referral, governance, groups, i18n, broadcast",
    "✅ V2 92%  achievements, AI, menu, progress, teaser, leaderboard",
    "✅ Notifications  mute/unmute, random daily reveal",
    "✅ Voting system  propose, vote, governance dashboard",
    "✅ Contacts  CSV upload, phone list import",
    "⏳ Partner system  15% commission, partner links",
    "⏳ Bulk messaging  send to contacts/groups",
    "⏳ Payments  Telegram Stars / USDT integration",
    "⏳ Onboarding flow  welcome messages, tutorial",
    "⏳ Final testing & launch prep",
]

@router.message(Command("tasks"))
async def tasks_cmd(message: types.Message):
    lines = ["📋 **Project Task List**"]
    lines.extend(PROJECT_TASKS)
    await message.answer('\n'.join(lines))
