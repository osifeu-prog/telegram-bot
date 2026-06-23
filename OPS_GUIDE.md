# 🛠️ SLH Bot  Operations Guide

## Quick Recovery
```powershell
cd D:\0\0.1\slh-telegram-bot
git pull origin main
railway up
Environment Variables (Railway)
BOT_TOKEN, DATABASE_URL, REDIS_URL, WEBHOOK_URL, MODE, ADMIN_ID, GITHUB_TOKEN, GROQ_API_KEY

Backup
Auto: /backup (admin)

Manual: Compress-Archive -Path src,static,locales,requirements.txt,railway.json -DestinationPath backups\slh-bot-$(Get-Date -Format 'yyyyMMdd-HHmmss').zip

Restore
git pull origin main

railway up

Adding New Features
Create handler in src/handlers/

Register router in src/webhook_server.py

Commit & push: git add . && git commit -m "New feature" && git push && railway up
