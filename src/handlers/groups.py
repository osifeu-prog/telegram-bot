from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()
ADMIN_ID = 8789977826

def is_admin(msg: types.Message) -> bool:
    return msg.from_user.id == ADMIN_ID

@router.message(Command("groups"))
async def list_groups(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    await message.answer("🔍 Scanning groups...")
    try:
        updates = await message.bot.get_updates(limit=100, timeout=10)
        groups = {}
        for update in updates:
            if update.message and update.message.chat:
                chat = update.message.chat
                if chat.type in ['group', 'supergroup']:
                    groups[chat.id] = chat.title
        if groups:
            msg_text = "📋 **Groups I'm in:**\n\n"
            for chat_id, title in groups.items():
                msg_text += f"• **{title}**\n  ID: `{chat_id}`\n\n"
        else:
            msg_text = "ℹ️ No groups found. Send a message in the group and try again."
        await message.answer(msg_text)
    except Exception as e:
        await message.answer(f"❌ Error: {e}")

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

@router.message(Command("group_services"))
async def group_services(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Broadcast to Group", callback_data="group_broadcast")],
        [InlineKeyboardButton(text="📊 Group Stats", callback_data="group_stats")],
        [InlineKeyboardButton(text="✅ KYC Members", callback_data="group_kyc")],
    ])
    await message.answer("🛠️ **Group Management Services**", reply_markup=keyboard)
