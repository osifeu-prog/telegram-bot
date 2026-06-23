import json
from pathlib import Path
from aiogram import Router, types
from aiogram.filters import Command
from src.bot.db.database import AsyncSessionLocal
from sqlalchemy import select, func
from src.bot.db.models import User

router = Router()
ADMIN_ID = 8789977826  # fallback

def is_admin(msg: types.Message) -> bool:
    return msg.from_user.id == ADMIN_ID

@router.message(Command("recalc_progress"))
async def recalc_progress_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return

    base = Path("src/handlers")
    feature_map_path = Path("ops/feature_map.json")
    status_path = Path("ops/system_status.json")

    # טען מיפוי
    try:
        feature_map = json.loads(feature_map_path.read_text(encoding="utf-8"))
    except:
        await message.answer("❌ feature_map.json missing or invalid.")
        return

    def check_feature(feat):
        handler = feat.get("handler")
        if handler:
            if not (base / handler).exists():
                return False
        # optionally check commands existence in the file (simplified)
        api = feat.get("api")
        if api and not (Path("src/api") / api).exists():
            return False
        static = feat.get("static")
        if static and not (Path("static") / static).exists():
            return False
        return True

    # חשב התקדמות
    progress = {"mvp": 0, "v1": 0, "v2": 0}
    for stage in ["mvp", "v1", "v2"]:
        feats = feature_map.get(stage, {})
        if not feats:
            progress[stage] = 1.0
            continue
        done = sum(1 for f in feats.values() if check_feature(f))
        progress[stage] = done / len(feats)

    # DB stats
    async with AsyncSessionLocal() as session:
        total_users = (await session.execute(select(func.count(User.telegram_id)))).scalar() or 0

    # שמור קובץ
    status = {
        "files": {f.name.split('.')[0]: True for f in base.glob("*.py")},
        "features": {},
        "admin": {"admin_status": True, "check_files": True, "run_tests": True, "deploy_status": True},
        "progress": {k: round(v, 2) for k, v in progress.items()},
        "total_users": total_users
    }
    status_path.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")

    await message.answer(
        f"✅ Progress recalculated!\n"
        f"MVP: {progress['mvp']*100:.0f}%\n"
        f"V1: {progress['v1']*100:.0f}%\n"
        f"V2: {progress['v2']*100:.0f}%\n"
        f"Total users: {total_users}"
    )
