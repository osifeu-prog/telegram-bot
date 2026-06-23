# SLH Telegram Bot  System Documentation

## Status: ✅ Active
- **Date:** 2026-06-23
- **Service:** Telegram_bot
- **URL:** https://telegrambot-production-a4c0.up.railway.app
- **Webhook:** POST /webhook → 200 OK
- **DB:** PostgreSQL (Railway Postgres)
- **Redis:** Redis (Railway Redis)

---

## Project Structure
src/
webhook_server.py  FastAPI + aiogram entry point
router_loader.py  Router setup
bot/
handlers/
admin_ops.py  Admin commands (/whoami, /status, /fix_db, /ops...)
db/
database.py  Async engine & session
fsm_storage.py  Redis FSM storage
models.py  User, Purchase models
handlers/
daily.py  Daily reward (/daily, /balance, /top)
payments.py  Payment handlers (Stars)
api/
mini_app.py  Mini App API endpoints
static/
index.html  Mini App HTML


---

## Commands

### User
- `/start`  Welcome message
- `/daily`  Claim daily reward (coins + streak)
- `/balance`  Check coins & streak
- `/top`  Leaderboard
- `/whoami`  User ID info

### Admin
- `/ops`  Admin menu
- `/status`  Health endpoint check
- `/health`  Service health
- `/fix_db`  Recreate users table
- `/deploy`  Trigger Railway deploy (requires hook URL)
- `/handoff`  Show session handoff doc
- `/tree`  Project file tree
- `/cat <path>`  View file contents

---

## Environment Variables (Railway)
- `BOT_TOKEN`
- `DATABASE_URL`
- `REDIS_URL`
- `WEBHOOK_URL`
- `WEBHOOK_MODE`
- `MODE` (PROD)
- `ADMIN_ID`
- `RAILWAY_DEPLOY_HOOK_URL`

---

## Database Schema

### users
| Column | Type | Default |
|--------|------|---------|
| telegram_id | BIGINT PK | |
| coins | INTEGER | 0 |
| current_streak | INTEGER | 0 |
| last_daily | TIMESTAMPTZ | NULL |
| boosts_available | INTEGER | 0 |
| created_at | TIMESTAMPTZ | now() |

### purchases
| Column | Type |
|--------|------|
| id | SERIAL PK |
| telegram_id | BIGINT |
| item | VARCHAR(50) |
| amount_stars | INTEGER |
| payload | VARCHAR(100) |
| created_at | TIMESTAMPTZ |

---

## Deployment
- **Platform:** Railway
- **Builder:** Railpack (Python)
- **Start Command:** `uvicorn src.webhook_server:app --host 0.0.0.0 --port $PORT`
- **Build Command:** `pip install -r requirements.txt`

---

## Quick Recovery
```powershell
cd D:\0\0.1\slh-telegram-bot
git pull origin main
railway up
Token Rotation
powershell
# BotFather → Revoke → Copy new token
railway variables --set "BOT_TOKEN=<NEW_TOKEN>" --service Telegram_bot
railway up
