# ROADMAP - Telegram Bot Integration & SLH_OS Control

## Current State
- Bot (@SLH_investor_wallet_bot) is running in background with aiogram.
- Direct PowerShell script execution for /progress, /health, /tasks, /board, /start_task, /done_task.
- Stable token handling and .env loading.
- Agents can log activity and update board via bot commands.
- Multiple tasks in progress across App, slh-telegram-bot, and revived bots.

## Pending Actions
1. Add /log <agent> "<message>" and /block_task <id> [reason] commands to bot.
2. Implement auto-restart watchdog (run_bot_bg.cmd) with health monitoring.
3. Complete full E2E testing of bot commands against live SLH_OS (especially task management).

## Blockers
- Need confirmation that only one bot instance is running to avoid TelegramConflictError.
- Staging DATABASE_URL / REDIS_URL + logs for full App auth verification (related to ID=33).
- Some slh commands still return "Command not found" in certain subprocess contexts.

## Knowledge Base
- Project path: D:\0\0.1\slh-telegram-bot
- venv: .\venv_fix\Scripts\python.exe
- Main file: bot_commands.py (direct script calls)
- SLH_OS core: S:\SLH_OS\scripts\slh.ps1 + commands\*
- Database: Railway PostgreSQL (asyncpg)
- Board: S:\SLH_OS\SYSTEM_BOARD.md

## Succession
- Day 1: Run slh board + slh progress, review open tasks in slh-telegram-bot and App.
- Check .env token and start bot with run_bot_bg.cmd.
- Always use direct -File calls to ps1 scripts for reliability in subprocess.
- Log every change and keep SYSTEM_BOARD.md as single source of truth.
