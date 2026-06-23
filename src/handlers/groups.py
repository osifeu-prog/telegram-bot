from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from sqlalchemy import select
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import GroupSettings
import re

router = Router()

# ------------------------------------------------------------
# ADMIN COMMANDS (group only)
# ------------------------------------------------------------
def is_group_admin(chat_id: int, user_id: int) -> bool:
    # In production you'd check via Telegram API.
    # For now we trust the user (simplified).
    return True

@router.message(Command("set_welcome"))
async def set_welcome_cmd(message: types.Message):
    if message.chat.type == "private":
        await message.answer("This command works only in groups.")
        return
    if not is_group_admin(message.chat.id, message.from_user.id):
        await message.answer("Only admins can set welcome.")
        return
    text = message.text.removeprefix("/set_welcome ").strip()
    if not text:
        await message.answer("Usage: /set_welcome <message>")
        return
    async with AsyncSessionLocal() as session:
        settings = await session.get(GroupSettings, message.chat.id)
        if not settings:
            settings = GroupSettings(chat_id=message.chat.id)
            session.add(settings)
        settings.welcome_message = text
        await session.commit()
    await message.answer("✅ Welcome message set!")

@router.message(Command("set_rules"))
async def set_rules_cmd(message: types.Message):
    if message.chat.type == "private":
        await message.answer("This command works only in groups.")
        return
    if not is_group_admin(message.chat.id, message.from_user.id):
        await message.answer("Only admins can set rules.")
        return
    text = message.text.removeprefix("/set_rules ").strip()
    if not text:
        await message.answer("Usage: /set_rules <rules>")
        return
    async with AsyncSessionLocal() as session:
        settings = await session.get(GroupSettings, message.chat.id)
        if not settings:
            settings = GroupSettings(chat_id=message.chat.id)
            session.add(settings)
        settings.rules = text
        await session.commit()
    await message.answer("✅ Rules updated!")

@router.message(Command("rules"))
async def rules_cmd(message: types.Message):
    if message.chat.type == "private":
        await message.answer("This command works only in groups.")
        return
    async with AsyncSessionLocal() as session:
        settings = await session.get(GroupSettings, message.chat.id)
    if not settings or not settings.rules:
        await message.answer("No rules set for this group.")
    else:
        await message.answer(f"📜 **Group Rules**\n{settings.rules}")

@router.message(Command("group_info"))
async def group_info_cmd(message: types.Message):
    if message.chat.type == "private":
        await message.answer("This command works only in groups.")
        return
    async with AsyncSessionLocal() as session:
        settings = await session.get(GroupSettings, message.chat.id)
    welcome = settings.welcome_message if settings else None
    rules = settings.rules if settings else None
    await message.answer(
        f"📋 **Group Info**\n"
        f"Chat ID: {message.chat.id}\n"
        f"Welcome: {'✅' if welcome else '❌'}\n"
        f"Rules: {'✅' if rules else '❌'}"
    )

@router.message(Command("ban"))
async def ban_cmd(message: types.Message):
    if message.chat.type == "private":
        await message.answer("This command works only in groups.")
        return
    if not is_group_admin(message.chat.id, message.from_user.id):
        await message.answer("Only admins can ban.")
        return
    # Ban by replying to user
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        await message.bot.ban_chat_member(message.chat.id, user_id)
        await message.answer("🔨 User banned.")
    else:
        await message.answer("Reply to a user's message with /ban to ban them.")

@router.message(Command("mute"))
async def mute_cmd(message: types.Message):
    if message.chat.type == "private":
        await message.answer("This command works only in groups.")
        return
    if not is_group_admin(message.chat.id, message.from_user.id):
        await message.answer("Only admins can mute.")
        return
    if not message.reply_to_message:
        await message.answer("Reply to a user's message with /mute.")
        return
    user_id = message.reply_to_message.from_user.id
    # Mute for 5 minutes by default (you can parse argument)
    await message.bot.restrict_chat_member(message.chat.id, user_id, permissions=types.ChatPermissions(can_send_messages=False))
    await message.answer("🔇 User muted (until manually unmuted).")

@router.message(Command("unban"))
async def unban_cmd(message: types.Message):
    if message.chat.type == "private":
        await message.answer("This command works only in groups.")
        return
    if not is_group_admin(message.chat.id, message.from_user.id):
        await message.answer("Only admins can unban.")
        return
    if not message.reply_to_message:
        await message.answer("Reply to a banned user's message (or previous message) with /unban.")
        return
    user_id = message.reply_to_message.from_user.id
    await message.bot.unban_chat_member(message.chat.id, user_id)
    await message.answer("✅ User unbanned.")

# ------------------------------------------------------------
# AUTO‑WELCOME (on new chat member)
# ------------------------------------------------------------
@router.message(lambda msg: msg.new_chat_members is not None)
async def welcome_new_member(message: types.Message):
    async with AsyncSessionLocal() as session:
        settings = await session.get(GroupSettings, message.chat.id)
    welcome = settings.welcome_message if settings else None
    for member in message.new_chat_members:
        if welcome:
            await message.answer(f"👋 {member.full_name}, {welcome}")
        else:
            await message.answer(f"👋 Welcome {member.full_name}!")

# ------------------------------------------------------------
# GROUP MESSAGE TRACKING (optional  log)
# ------------------------------------------------------------
@router.message()
async def log_group_activity(message: types.Message):
    # Simply acknowledge; you could log to DB
    pass
