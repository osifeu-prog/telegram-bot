import uuid
from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("missions"))
async def missions_cmd(message: types.Message):
    await message.answer(
        "ðŸ“‹ **Missions**\n"
        "â€¢ Daily Login  Collect your reward with /daily\n"
        "â€¢ Invite Friends  Share the bot and earn bonuses\n"
        "â€¢ Vote  Participate in community decisions with /vote\n"
        "â€¢ Shop  Buy boosts and items with /shop"
    )

@router.message(Command("tutorial"))
async def tutorial_cmd(message: types.Message):
    await message.answer(
        "ðŸ“˜ **Tutorial**\n\n"
        "1ï¸âƒ£ Start with /daily every day to earn coins.\n"
        "2ï¸âƒ£ Build your streak  longer streaks = bigger rewards.\n"
        "3ï¸âƒ£ Use /balance to check your progress.\n"
        "4ï¸âƒ£ Compete on the /top leaderboard.\n"
        "5ï¸âƒ£ Visit the /shop to buy boosts.\n"
        "6ï¸âƒ£ Vote on community decisions to shape the economy.\n\n"
        "â“ Need help? Use /faq or /contact."
    )

@router.message(Command("faq"))
async def faq_cmd(message: types.Message):
    await message.answer(
        "â“ **FAQ**\n\n"
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
        "ðŸ“§ **Contact**\n"
        "Admin: @Osif\n"
        "Support group: coming soon\n"
        "Report issues: /bug <description>"
    )



# ---------- Partner & Tasks & Contacts ----------
@router.message(Command("partner_register"))
async def partner_register_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()
        if not user:
            await message.answer("You must /start first.")
            return
        try:
            _ = user.partner_code
        except AttributeError:
            await message.answer("System update in progress. Try again in a minute.")
            return
        if user.partner_code:
            await message.answer(f"You are already a partner! Code: `{user.partner_code}`")
            return
        user.partner_code = uuid.uuid4().hex[:8]
        session.add(user)
        await session.commit()
    bot_username = (await message.bot.get_me()).username
    ref_link = f"https://t.me/{bot_username}?start=ref_{message.from_user.id}"
    await message.answer(
        f"🎉 You are now a partner!\n"
        f"Your referral link: {ref_link}\n"
        f"Commission: {user.partner_commission}%\n"
        f"Share it to earn!"
    )

@router.message(Command("partner_stats"))
async def partner_stats_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, message.from_user.id)
        if not user or not getattr(user, 'partner_code', None):
            await message.answer("You are not a partner yet. Use /partner_register.")
            return
        result = await session.execute(
            select(func.count(User.telegram_id)).where(User.referrer_id == message.from_user.id)
        )
        referral_count = result.scalar()
    await message.answer(
        f"📊 **Partner Stats**\n"
        f"Referrals: {referral_count}\n"
        f"Commission rate: {user.partner_commission}%\n"
        f"Your code: `{user.partner_code}`"
    )

@router.message(Command("tasks"))
async def tasks_cmd(message: types.Message):
    tasks_list = [
        "✅ MVP 100%  daily loop, wallet, shop, mini-app",
        "✅ V1 95%  KYC, referral, governance, groups, i18n, broadcast",
        "✅ V2 92%  achievements, AI, menu, progress, teaser, leaderboard",
        "✅ Notifications  mute/unmute, random daily reveal",
        "✅ Voting system  propose, vote, governance dashboard",
        "✅ Contacts  CSV upload, phone list import",
        "✅ Partner system  15% commission, partner links",
        "⏳ Bulk messaging  send to contacts/groups",
        "⏳ Payments  Telegram Stars / USDT integration",
        "⏳ Onboarding flow  welcome messages, tutorial",
        "⏳ Final testing & launch prep",
    ]
    await message.answer("📋 **Project Task List**\n" + "\n".join(tasks_list))

@router.message(Command("contacts_list"))
async def contacts_list_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Contact).where(Contact.owner_id == message.from_user.id).limit(50)
        )
        contacts = result.scalars().all()
    if not contacts:
        await message.answer("No contacts found. Upload a CSV/VCF with /upload_contacts.")
        return
    lines = ["📋 **Your Contacts**"]
    for c in contacts:
        lines.append(f"{c.phone}  {c.name or 'N/A'} [{c.group_name or '-'}]")
    await message.answer('\n'.join(lines))

