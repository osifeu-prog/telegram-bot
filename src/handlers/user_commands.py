from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("missions"))
async def missions_cmd(message: types.Message):
    await message.answer(
        "📋 **Missions**\n"
        "• Daily Login  Collect your reward with /daily\n"
        "• Invite Friends  Share the bot and earn bonuses\n"
        "• Vote  Participate in community decisions with /vote\n"
        "• Shop  Buy boosts and items with /shop"
    )

@router.message(Command("tutorial"))
async def tutorial_cmd(message: types.Message):
    await message.answer(
        "📘 **Tutorial**\n\n"
        "1️⃣ Start with /daily every day to earn coins.\n"
        "2️⃣ Build your streak  longer streaks = bigger rewards.\n"
        "3️⃣ Use /balance to check your progress.\n"
        "4️⃣ Compete on the /top leaderboard.\n"
        "5️⃣ Visit the /shop to buy boosts.\n"
        "6️⃣ Vote on community decisions to shape the economy.\n\n"
        "❓ Need help? Use /faq or /contact."
    )

@router.message(Command("faq"))
async def faq_cmd(message: types.Message):
    await message.answer(
        "❓ **FAQ**\n\n"
        "Q: How do I earn coins?\n"
        "A: Use /daily every 24 hours.\n\n"
        "Q: What is a streak?\n"
        "A: Consecutive days claiming your daily reward.\n\n"
        "Q: How do boosts work?\n"
        "A: Purchase them in /shop to protect your streak.\n\n"
        "Q: How do I vote?\n"
        "A: Use /vote when a proposal is open.\n\n"
        "More questions? Use /contact."
    )

@router.message(Command("contact"))
async def contact_cmd(message: types.Message):
    await message.answer(
        "📧 **Contact**\n"
        "Admin: @Osif\n"
        "Support group: coming soon\n"
        "Report issues: /bug <description>"
    )

