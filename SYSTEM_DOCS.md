# 🚀 SLH Telegram Bot  Complete Development Kit
**Date:** 2026-06-23  
**Status:** ✅ Production Ready  
**URL:** https://telegrambot-production-a4c0.up.railway.app

---

## 🧭 Quick Start
```powershell
cd D:\0\0.1\slh-telegram-bot
git pull origin main
railway up
📋 All Commands
User Commands
/start /daily /balance /top /missions /tutorial /faq /contact
/wallet /set_wallet <addr> /deposit /report_deposit <hash> <amount>
/profile /prices /shop /buy /premium /demo_deposit <amount>

Admin Commands
/ops /whoami /status /health /fix_db /deploy
/user_info <id> /user_reset <id> /ban /unban
/economy_status /reward_add <id> <amt> /token_mint <amt>
/vote_create <q> /vote /vote_close <id> /vote_stats
/confirm_deposit <id> /verify_deposit <id>

DevOps Commands
/logs_tail /cpu /ram /git_status /tree /cat <path>

📁 Project Structure

src/
  webhook_server.py       Main entry point
  router_loader.py        Router setup
  bot/
    handlers/admin_ops.py  Admin commands
    db/database.py         Async engine & session
    db/fsm_storage.py      Redis FSM storage
    db/models.py           User, Purchase, SystemConfig
  handlers/
    daily.py               Daily reward
    payments.py            Payment handlers
    user_commands.py       /missions, /tutorial, /faq, /contact
    shop.py                /shop, /buy, /premium
    admin_users.py         /user_info, /user_reset
    admin_economy.py       /economy_status, /reward_add, /token_mint
    devops.py              /logs_tail, /cpu, /ram, /git_status
    governance.py          /vote_create, /vote, /vote_close, /vote_stats
    wallet.py              /wallet, /set_wallet, /deposit
    deposits.py            /report_deposit, /confirm_deposit, /verify_deposit
    profile.py             /profile, /prices
    demo.py                /demo_deposit
  api/
    mini_app.py            Mini App API endpoints
  services/
    ton.py                 TON blockchain integration
    notifications.py       Daily reminders
  scripts/
    seed_users.py          Seed 100 demo users
static/
  index.html               Mini App Dashboard
🗄️ Database Schema
users
ColumnTypeDefault
telegram_idBIGINT PK
coinsINTEGER0
current_streakINTEGER0
last_dailyTIMESTAMPTZNULL
boosts_availableINTEGER0
wallet_addressVARCHAR(100)NULL
roleVARCHAR(20)'user'
is_kycBOOLEANFALSE
created_atTIMESTAMPTZnow()
purchases
ColumnType
idSERIAL PK
telegram_idBIGINT
itemVARCHAR(50)
amount_usdtINTEGER
tx_hashVARCHAR(100)
statusVARCHAR(20)
created_atTIMESTAMPTZ
system_config
ColumnType
keyVARCHAR(50) PK
valueVARCHAR(500)
🔗 Integrations
TON Blockchain: /verify_deposit checks TON Center API

GitHub: /deploy triggers GitHub Deployments API

Railway: Auto-deploy on push to main

🧪 Test Mode
/demo_deposit <amount>  Adds demo coins instantly

100 demo users can be seeded: railway run python src/scripts/seed_users.py

🔐 Security
Admin-only commands protected by ADMIN_ID

System wallet stored in DB (system_config)

Token rotated via BotFather → railway variables --set "BOT_TOKEN=..."

📦 Backup
Backups stored in backups/ and pushed to GitHub.
