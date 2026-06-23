from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import GroupInfo

router = Router()
ADMIN_ID = 8789977826

def is_admin(msg: types.Message) -> bool:
    return msg.from_user.id == ADMIN_ID

# Handler for when bot is added to a group
@router.my_chat_member()
async def bot_added_to_group(event: types.ChatMemberUpdated):
    if event.new_chat_member.status == "member" and event.new_chat_member.user.id == event.bot.id:
        chat = event.chat
        if chat.type in ['group', 'supergroup']:
            async with AsyncSessionLocal() as session:
                exists = await session.get(GroupInfo, chat.id)
                if not exists:
                    session.add(GroupInfo(id=chat.id, title=chat.title, type=chat.type))
                    await session.commit()

@router.message(Command("groups"))
async def list_groups(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(GroupInfo).order_by(GroupInfo.added_at.desc()))
        groups = result.scalars().all()
    if groups:
        msg_text = "📋 **Groups I'm in:**\n\n"
        for g in groups:
            msg_text += f"• **{g.title}**\n  ID: `{g.id}`\n\n"
    else:
        msg_text = "ℹ️ No groups recorded. Add the bot to a group and send a message."
    await message.answer(msg_text)

@router.message(Command("group_id"))
async def get_group_id(message: types.Message):
    chat = message.chat
    await message.answer(
        f"📋 **Chat Info**\n"
        f"Type: {chat.type}\n"
        f"Title: {chat.title or 'N/A'}\n"
        f"ID: `{chat.id}`"
    )

@router.message(Command("add_to_group"))
async def add_to_group_info(message: types.Message):
    await message.answer(
        "🤝 **Add SLH Bot to Your Group**\n\n"
        "1️⃣ Add @SLH_investor_wallet_bot to your group\n"
        "2️⃣ Make the bot an **admin**\n"
        "3️⃣ Send /group_id to get the Group ID\n"
        "4️⃣ Use /groups to see all groups\n\n"
        "🏆 **Benefits:** Daily rewards, Voting, Economy, KYC"
    )
