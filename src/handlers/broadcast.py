import csv, os
from io import StringIO
from aiogram import Router, types
from aiogram.filters import Command

router = Router()
ADMIN_ID = 8789977826

def is_admin(msg: types.Message) -> bool:
    return msg.from_user.id == ADMIN_ID

@router.message(Command("broadcast"))
async def broadcast_help(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    await message.answer(
        "📢 **Broadcast Tool**\n\n"
        "Send a CSV file with phone numbers to invite users.\n"
        "CSV format: one column `phone` (international format, e.g. +972501234567)\n\n"
        "Commands:\n"
        "/broadcast_preview <csv_file>  Preview list\n"
        "/broadcast_send <csv_file>  Send Telegram invites"
    )

@router.message(Command("broadcast_preview"))
async def broadcast_preview(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    # This is triggered when user sends a document after the command
    await message.answer("Please send the CSV file now.")

@router.message(lambda msg: msg.document is not None)
async def handle_csv(message: types.Message):
    if not is_admin(message):
        return
    if not message.document.file_name.endswith('.csv'):
        await message.answer("Only CSV files are accepted.")
        return
    
    file = await message.bot.get_file(message.document.file_id)
    file_bytes = await message.bot.download_file(file.file_path)
    content = file_bytes.read().decode('utf-8')
    reader = csv.reader(StringIO(content))
    phones = [row[0].strip() for row in reader if row and row[0].strip().startswith('+')]
    
    preview = "📋 **Preview**\n"
    for i, p in enumerate(phones[:10], 1):
        preview += f"{i}. {p}\n"
    if len(phones) > 10:
        preview += f"... and {len(phones)-10} more\n"
    preview += f"\nTotal: {len(phones)} contacts.\n\nUse /broadcast_send <filename> to send."
    await message.answer(preview)

@router.message(Command("broadcast_send"))
async def broadcast_send(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    # Get the last CSV file sent
    await message.answer("Sending invites... (simulated)\n\nIn real mode, this would send Telegram messages to contacts.")
    # In production, you would look up contacts by phone and send them a Telegram message.
