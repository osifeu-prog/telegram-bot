from aiogram import Router, types
from aiogram.filters import Command
import csv
from io import StringIO

router = Router()
ADMIN_ID = 8789977826

def is_admin(msg: types.Message) -> bool:
    return msg.from_user.id == ADMIN_ID

@router.message(Command("import_contacts"))
async def import_contacts_help(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    await message.answer(
        "📲 **Import Contacts**\n\n"
        "Send a CSV file with phone numbers (one per line or column `phone`).\n"
        "I'll store them for future SMS invitations.\n\n"
        "SMS sending requires an SMS gateway (Twilio, etc.)  coming soon."
    )

@router.message(Command("sms_invite"))
async def sms_invite_info(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    await message.answer(
        "💬 **SMS Invites**\n\n"
        "This feature is under development.\n"
        "It will send an SMS to imported contacts, inviting them to join via Telegram.\n"
        "We will use an SMS gateway API (e.g., Twilio).\n\n"
        "Roadmap: V2.1"
    )
