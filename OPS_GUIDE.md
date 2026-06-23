# 🛠️ SLH Bot  Operations Guide

## Quick Recovery
```powershell
cd D:\0\0.1\slh-telegram-bot
git pull origin main
railway up
Environment Variables (Railway)
VariableDescription
BOT_TOKENTelegram bot token
DATABASE_URLPostgreSQL connection string
REDIS_URLRedis connection string
WEBHOOK_URLhttps://telegrambot-production-a4c0.up.railway.app/webhook
MODEPROD or DEV
ADMIN_IDYour Telegram user ID (8789977826)
GITHUB_TOKENFor /deploy command
AI_API_KEY(Optional) For /ask_ai command
Backup
Auto backup: /backup (admin)

Manual: Compress-Archive -Path src,static,locales,requirements.txt,railway.json -DestinationPath backups\slh-bot-$(Get-Date -Format 'yyyyMMdd-HHmmss').zip

Restore
git pull origin main

railway up

Token Rotation
@BotFather → Revoke token

railway variables --set "BOT_TOKEN=<new>" --service Telegram_bot

railway up

Adding New Language
Create locales/xx.json (copy from en.json)

Translate all values

Deploy: git add locales/ && git commit -m "Add xx language" && git push && railway up

Troubleshooting
Bot not responding: Check webhook: /health, /status

DB errors: Run /fix_db

Deploy failed: Check railway logs --deployment latest
