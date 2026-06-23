import os
import httpx
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

def is_admin(msg: Message) -> bool:
    return msg.from_user.id == ADMIN_ID

@router.message(Command("whoami"))
async def whoami(msg: Message):
    await msg.reply(
        f"?? Your ID: `{msg.from_user.id}`\n"
        f"?? Username: @{msg.from_user.username or 'N/A'}\n"
        f"?? Chat ID: `{msg.chat.id}`\n"
        f"?? Chat type: {msg.chat.type}"
    )

@router.message(Command("status"))
async def status_cmd(msg: Message):
    if not is_admin(msg):
        await msg.reply("? Access denied.")
        return
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://telegrambot-production-a4c0.up.railway.app/")
        text = resp.text
    await msg.reply(f"?? Health endpoint:\n`{text}`")

@router.message(Command("health"))
async def health_cmd(msg: Message):
    if not is_admin(msg):
        await msg.reply("? Access denied.")
        return
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://telegrambot-production-a4c0.up.railway.app/")
        ok = resp.status_code == 200
    await msg.reply(f"?? Health: {'? Online' if ok else '? Down'} (HTTP {resp.status_code})")

@router.message(Command("deploy"))
async def deploy_cmd(msg: Message):
    if not is_admin(msg):
        await msg.reply("? Access denied.")
        return
    hook_url = os.getenv("RAILWAY_DEPLOY_HOOK_URL")
    if not hook_url:
        await msg.reply("? RAILWAY_DEPLOY_HOOK_URL not set.")
        return
    async with httpx.AsyncClient() as client:
        resp = await client.post(hook_url)
        if resp.status_code == 200:
            await msg.reply("?? Deploy triggered!")
        else:
            await msg.reply(f"? Deploy trigger failed (HTTP {resp.status_code})")

@router.message(Command("handoff"))
async def handoff_cmd(msg: Message):
    if not is_admin(msg):
        await msg.reply("? Access denied.")
        return
    try:
        with open("ops/SESSION_HANDOFF_20260623.md", "r", encoding="utf-8") as f:
            text = f.read()
        await msg.reply(f"?? Session Handoff:\n```\n{text[:4000]}\n```")
    except FileNotFoundError:
        await msg.reply("? Handoff file not found.")

@router.message(Command("tree"))
async def tree_cmd(msg: Message):
    if not is_admin(msg):
        await msg.reply("? Access denied.")
        return
    import subprocess
    try:
        res = subprocess.run(["tree", "/app", "-L", "2"], capture_output=True, text=True, timeout=10)
        output = res.stdout[:3900]
        await msg.reply(f"?? Project tree:\n```\n{output}\n```")
    except Exception as e:
        await msg.reply(f"? Error: {e}")

@router.message(Command("cat"))
async def cat_cmd(msg: Message):
    if not is_admin(msg):
        await msg.reply("? Access denied.")
        return
    # usage: /cat src/webhook_server.py
    path = msg.text.split(" ", 1)[1] if len(msg.text.split()) > 1 else ""
    if not path:
        await msg.reply("Usage: /cat <path>")
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()[:3500]
        await msg.reply(f"?? {path}:\n```\n{content}\n```")
    except Exception as e:
        await msg.reply(f"? {e}")

@router.message(Command("ops"))
async def ops_menu(msg: Message):
    if not is_admin(msg):
        await msg.reply("? Access denied.")
        return
    menu = (
        "?? **Admin Command Center**\n"
        "/whoami  Get user ID\n"
        "/status  Health endpoint\n"
        "/health  Check service\n"
        "/deploy  Trigger deployment\n"
        "/handoff  Show handoff doc\n"
        "/tree  Directory structure\n"
        "/cat  View file\n"
        "/ops  This menu"
    )
    await msg.reply(menu)
