import os, subprocess
from aiogram import Router, types
from aiogram.filters import Command

router = Router()
ADMIN_ID = 8789977826

def is_admin(msg: types.Message) -> bool:
    return msg.from_user.id == ADMIN_ID

@router.message(Command("logs_tail"))
async def logs_tail_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    try:
        output = subprocess.check_output("tail -50 /var/log/*.log 2>/dev/null || echo 'No logs found'", shell=True, text=True)
        await message.answer(f"📋 Logs:\n```\n{output[:3000]}\n```")
    except Exception as e:
        await message.answer(f"❌ {e}")

@router.message(Command("cpu"))
async def cpu_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    try:
        output = subprocess.check_output("top -bn1 | head -5", shell=True, text=True)
        await message.answer(f"🖥 CPU:\n```\n{output[:1000]}\n```")
    except Exception as e:
        await message.answer(f"❌ {e}")

@router.message(Command("ram"))
async def ram_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    try:
        output = subprocess.check_output("free -m", shell=True, text=True)
        await message.answer(f"🧠 RAM:\n```\n{output[:1000]}\n```")
    except Exception as e:
        await message.answer(f"❌ {e}")

@router.message(Command("git_status"))
async def git_status_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    try:
        status = subprocess.check_output("git status", shell=True, text=True, cwd="/app")
        log = subprocess.check_output("git log --oneline -5", shell=True, text=True, cwd="/app")
        await message.answer(f"📂 Git Status:\n```\n{status[:1000]}\n```\n📜 Recent:\n```\n{log[:1000]}\n```")
    except Exception as e:
        await message.answer(f"❌ {e}")

