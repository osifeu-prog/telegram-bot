import os, subprocess
from datetime import datetime
from aiogram import Router, types
from aiogram.filters import Command

router = Router()
ADMIN_ID = 8789977826

def is_admin(msg: types.Message) -> bool:
    return msg.from_user.id == ADMIN_ID

@router.message(Command("backup"))
async def backup_cmd(message: types.Message):
    if not is_admin(message):
        await message.reply("⛔ Access denied.")
        return
    await message.reply("🔄 Creating backup...")
    try:
        timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        filename = f"backups/slh-bot-backup-{timestamp}.zip"
        subprocess.run(
            f"zip -r {filename} src static locales requirements.txt railway.json -x '*__pycache__*'",
            shell=True, cwd="/app", check=True
        )
        # Push to Git (optional)
        subprocess.run("git add backups/ && git commit -m 'Auto backup' && git push", shell=True, cwd="/app")
        await message.reply(f"✅ Backup created: {filename}")
    except Exception as e:
        await message.reply(f"❌ Backup failed: {e}")

@router.message(Command("ask_ai"))
async def ask_ai_cmd(message: types.Message):
    if not is_admin(message):
        await message.reply("⛔ Access denied.")
        return
    prompt = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else ""
    if not prompt:
        await message.reply("Usage: /ask_ai <your prompt>")
        return
    # Placeholder  Replace with actual AI API call
    await message.reply(f"🤖 Your prompt: \"{prompt}\"\n\nAI response: (API not configured yet. Set AI_API_KEY in Railway.)")
