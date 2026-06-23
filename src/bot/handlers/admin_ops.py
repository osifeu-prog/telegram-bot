import os
import httpx
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

def is_admin(msg: Message) -> bool:
    return msg.from_user.id == ADMIN_ID

@router.message(Command("whoami"))
async def whoami(msg: Message):
    await msg.reply(
        f"👤 Your ID: `{msg.from_user.id}`\n"
        f"📛 Username: @{msg.from_user.username or 'N/A'}\n"
        f"💬 Chat ID: `{msg.chat.id}`\n"
        f"👥 Chat type: {msg.chat.type}"
    )

@router.message(Command("status"))
async def status_cmd(msg: Message):
    if not is_admin(msg):
        await msg.reply("⛔ Access denied.")
        return
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://telegrambot-production-a4c0.up.railway.app/")
        text = resp.text
    await msg.reply(f"🌐 Health endpoint:\n`{text}`")

@router.message(Command("health"))
async def health_cmd(msg: Message):
    if not is_admin(msg):
        await msg.reply("⛔ Access denied.")
        return
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://telegrambot-production-a4c0.up.railway.app/")
        ok = resp.status_code == 200
    await msg.reply(f"🩺 Health: {'✅ Online' if ok else '❌ Down'} (HTTP {resp.status_code})")

@router.message(Command("deploy"))
async def deploy_cmd(msg: Message):
    if not is_admin(msg):
        await msg.reply("⛔ Access denied.")
        return
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        await msg.reply("❌ GITHUB_TOKEN not set.")
        return
    import httpx
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"ref": "main"}
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.github.com/repos/osifeu-prog/telegram-bot/deployments",
            headers=headers,
            json=data
        )
        if resp.status_code == 201:
            await msg.reply("🚀 Deploy triggered via GitHub!")
        else:
            await msg.reply(f"❌ Failed (HTTP {resp.status_code})")
@router.message(Command("handoff"))
async def handoff_cmd(msg: Message):
    if not is_admin(msg):
        await msg.reply("⛔ Access denied.")
        return
    try:
        with open("ops/SESSION_HANDOFF_20260623.md", "r", encoding="utf-8") as f:
            text = f.read()
        await msg.reply(f"📋 Session Handoff:\n```\n{text[:4000]}\n```")
    except FileNotFoundError:
        await msg.reply("❌ Handoff file not found.")

@router.message(Command("tree"))
async def tree_cmd(msg: Message):
    if not is_admin(msg):
        await msg.reply("⛔ Access denied.")
        return
    import os as _os
    lines = []
    for root, dirs, files in _os.walk("/app"):
        level = root.replace("/app", "").count(_os.sep)
        indent = "  " * level
        lines.append(f"{indent}{_os.path.basename(root)}/")
        for file in files[:10]:
            lines.append(f"{indent}  {file}")
        if len(files) > 10:
            lines.append(f"{indent}  ...")
        if len(lines) > 100:
            break
    await msg.reply("📁 Project tree:\n```\n" + "\n".join(lines[:4000]) + "\n```")

@router.message(Command("cat"))
async def cat_cmd(msg: Message):
    if not is_admin(msg):
        await msg.reply("⛔ Access denied.")
        return
    parts = msg.text.split(" ", 1)
    path = parts[1] if len(parts) > 1 else ""
    if not path:
        await msg.reply("Usage: /cat <path>")
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()[:3500]
        await msg.reply(f"📄 {path}:\n```\n{content}\n```")
    except Exception as e:
        await msg.reply(f"❌ {e}")

@router.message(Command("fix_db"))
async def fix_db_cmd(msg: Message):
    if not is_admin(msg):
        await msg.reply("⛔ Access denied.")
        return
    from src.bot.db.database import engine
    from src.bot.db.models import Base, User
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all, tables=[User.__table__])
        await conn.run_sync(Base.metadata.create_all, tables=[User.__table__])
    await msg.reply("✅ Database fixed! Table `users` recreated with all columns.")

@router.message(Command("ops"))
async def ops_menu(msg: Message):
    if not is_admin(msg):
        await msg.reply("⛔ Access denied.")
        return
    await msg.reply(
        "🛠 **Admin Command Center**\n"
        "/whoami  Get user ID\n"
        "/status  Health endpoint\n"
        "/health  Check service\n"
        "/deploy  Trigger deployment\n"
        "/handoff  Show handoff doc\n"
        "/tree  Directory structure\n"
        "/cat  View file\n"
        "/fix_db  Recreate users table\n"
        "/ops  This menu"
    )

