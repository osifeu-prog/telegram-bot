# 🚀 SLH Telegram Bot  Complete System Documentation
**Date:** 2026-06-23 | **Status:** ✅ Production Ready  
**URL:** https://telegrambot-production-a4c0.up.railway.app

## 📋 All Commands

### User
/start /daily /balance /top /missions /tutorial /faq /contact
/wallet /set_wallet <addr> /deposit /report_deposit <hash> <amount>
/profile /prices /shop /buy /premium /demo_deposit <amount>
/language <en|he|ru|ar|es|fr>
/kyc /kyc_status /ref /achievements /testnet_wallet /testnet_deposit

### Admin
/ops /whoami /status /health /fix_db /deploy
/user_info <id> /user_reset <id> /ban /unban
/economy_status /reward_add <id> <amt> /token_mint <amt>
/vote_create <q> /vote /vote_close <id> /vote_stats
/confirm_deposit <id> /verify_deposit <id>
/kyc_approve <id>
/menu /progress /missing /roadmap /checklist /full_check
/backup /ask_ai <prompt> /analyze_pdf

### DevOps
/logs_tail /cpu /ram /git_status /tree /cat <path>

## 🌍 Languages
English, Hebrew, Russian, Arabic, Spanish, French

## 📁 Structure
src/
webhook_server.py, router_loader.py
bot/ (handlers/, db/)
handlers/ (daily, payments, user_commands, shop, admin_*, devops, governance, wallet, deposits, profile, demo, language, menu_system, ops_commands, pdf_analyzer, kyc, ton_testnet, referral, achievements, mini_app_improved)
api/ (mini_app.py)
services/ (ton.py, notifications.py)
scripts/ (seed_users.py)
utils/ (i18n.py)
static/ (index.html)
locales/ (en.json, he.json, ru.json, ar.json, es.json, fr.json)


## 🔗 Integrations
- TON Blockchain (verify deposits)
- TON Testnet (safe testing)
- GitHub (deploy trigger)
- Railway (auto-deploy on push)
- Groq AI (ask_ai, pdf analysis)

## 🔐 Security
- Admin-only commands via ADMIN_ID
- System wallet in DB (system_config)
- Token rotated via BotFather

## 📦 Backup
- Auto: /backup (admin)
- Manual: Compress-Archive in backups/
