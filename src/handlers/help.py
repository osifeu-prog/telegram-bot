from aiogram import Router, types
from aiogram.filters import Command
from src.utils.i18n import get_string

router = Router()

# מילון פקודות עם תיאור קצר (אנגלית  ה‑i18n יתרגם אוטומטית)
COMMANDS_INFO = {
    "start": "Register and get welcome bonus.",
    "daily": "Claim your daily reward.",
    "reward": "Get your daily bonus.",
    "streak": "Check your current daily streak.",
    "shop": "Open the digital shop.",
    "buy": "Purchase an item from the shop.",
    "profile": "View your profile and stats.",
    "wallet": "Show your USDT/TON wallet address.",
    "deposit": "Report a deposit.",
    "vote": "Vote on community proposals.",
    "governance": "View governance status.",
    "kyc": "Verify your identity.",
    "referral": "Get your referral link and stats.",
    "achievements": "View your achievements.",
    "language": "Change your language. Usage: /language <code>",
    "menu": "Show the main menu.",
    "demo": "Try demo features.",
    "pdf": "Analyze a PDF document.",
    "ton_testnet": "TON testnet functions.",
    "contacts": "Manage your contacts.",
    "broadcast": "(Admin) Send a broadcast message.",
    "groups": "Manage group settings.",
    "mini_app": "Launch the mini-app.",
    "teaser": "Show countdown and your Genesis Shards.",
    "daily_quest": "Complete the daily quest to earn shards.",
    "leaderboard": "View the top Genesis holders.",
    "admin_status": "(Admin) System status.",
    "check_files": "(Admin) Check critical files.",
    "run_tests": "(Admin) Run automated tests.",
    "deploy_status": "(Admin) Deployment status.",
    "admin_users": "(Admin) Manage users.",
    "admin_economy": "(Admin) Manage economy.",
    "ops": "Operational commands.",
    "progress": "View project progress.",
    "missing": "Show missing features/files.",
    "checklist": "Show checklist.",
    "full_check": "Full system health check.",
    "devops": "DevOps commands.",
    "db_status": "Database status.",
    "git_status": "Git repository status.",
    "logs": "View recent logs.",
    "backup": "Create a backup.",
    "help": "Show this help message.",
}

@router.message(Command("help"))
async def help_cmd(message: types.Message):
    args = message.text.split()
    lang = "en"  # או שליפה מ‑DB, כרגע ברירת מחדל
    if len(args) > 1:
        cmd = args[1].lstrip("/")
        info = COMMANDS_INFO.get(cmd)
        if info:
            await message.answer(f"📖 /{cmd}\n{info}")
        else:
            await message.answer("Unknown command. Use /help for full list.")
        return
    # תפריט כללי
    lines = ["📚 **Available Commands**\n"]
    for cmd, desc in COMMANDS_INFO.items():
        lines.append(f"/{cmd}  {desc}")
    await message.answer("\n".join(lines))
