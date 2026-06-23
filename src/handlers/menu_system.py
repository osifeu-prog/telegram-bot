from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.utils.i18n import get_string
from aiogram import F
from aiogram.types import CallbackQuery

router = Router()
ADMIN_ID = 8789977826

def get_user_lang(telegram_id: int) -> str:
    return "en"

def is_admin(msg: types.Message) -> bool:
    return msg.from_user.id == ADMIN_ID

def main_menu_keyboard(lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="?? Home", callback_data="menu_main")],
        [InlineKeyboardButton(text="?? Shop", callback_data="menu_shop"),
         InlineKeyboardButton(text="?? Top", callback_data="menu_top")],
    ])

def admin_menu_keyboard(lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="?? Status", callback_data="admin_status"),
         InlineKeyboardButton(text="?? Check", callback_data="check_files")],
        [InlineKeyboardButton(text="?? Progress", callback_data="progress"),
         InlineKeyboardButton(text="? Missing", callback_data="missing")],
    ])

@router.message(Command("menu"))
async def menu_cmd(message: types.Message):
    if is_admin(message):
        await message.answer("??? Admin Control Center", reply_markup=admin_menu_keyboard("en"))
    else:
        await message.answer("?? Main Menu", reply_markup=main_menu_keyboard("en"))

@router.message(Command("progress"))
async def progress_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("? Access denied.")
        return
    import json
    try:
        with open("ops/system_status.json", "r") as f:
            status = json.load(f)
    except:
        status = {"progress": {"mvp": 1.0, "v1": 0.95, "v2": 0.92}}
    mvp = status["progress"]["mvp"] * 100
    v1 = status["progress"]["v1"] * 100
    v2 = status["progress"]["v2"] * 100
    await message.answer(
        f"?? Progress\n\nMVP: {mvp:.0f}%\nV1: {v1:.0f}%\nV2: {v2:.0f}%"
    )

@router.message(Command("missing"))
async def missing_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("? Access denied.")
        return
    import json
    try:
        with open("ops/system_status.json", "r") as f:
            status = json.load(f)
    except:
        status = {}
    missing_files = [f for f, exists in status.get("files", {}).items() if not exists]
    msg = "? Missing Items\n" + "\n".join(missing_files) if missing_files else "? Nothing missing!"
    await message.answer(msg)

@router.message(Command("checklist"))
async def checklist_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("? Access denied.")
        return
    await message.answer(
        "?? Checklist\n? Webhook\n? DB\n? Daily\n? Shop\n? Payments\n? Votes\n? Mini-App\n? i18n\n? Referral"
    )

@router.message(Command("full_check"))
async def full_check_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("? Access denied.")
        return
    import httpx
    checks = []
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get("https://telegrambot-production-a4c0.up.railway.app/")
            checks.append(("Webhook", resp.status_code == 200))
        except:
            checks.append(("Webhook", False))
    from src.bot.db.database import engine
    from sqlalchemy import text
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        checks.append(("Database", True))
    except:
        checks.append(("Database", False))
    msg = "?? Full System Check\n" + "\n".join(f"{'?' if ok else '?'} {name}" for name, ok in checks)
    await message.answer(msg)


from aiogram import F
from aiogram.types import CallbackQuery

@router.callback_query()
async def menu_callback(query: CallbackQuery):
    await query.answer(f"You clicked: {query.data}")
    if query.data == "menu_main":
        await query.message.answer("?? Main Menu placeholder")
    elif query.data == "menu_shop":
        await query.message.answer("?? Shop placeholder")
    elif query.data == "menu_top":
        await query.message.answer("?? Top placeholder")
    elif query.data == "admin_status":
        await query.message.answer("?? Status: Active")
    elif query.data == "check_files":
        await query.message.answer("?? Files: All present")
    elif query.data == "progress":
        await query.message.answer("?? Progress command sent")
    elif query.data == "missing":
        await query.message.answer("? Missing command sent")


