@echo off
title SLH Bot Watchdog

echo Starting SLH Bot Watchdog...

:loop
tasklist /fi "imagename eq python.exe" /fo csv | findstr /i "bot_commands.py" >nul
if %errorlevel% neq 0 (
    echo [%date% %time%] Bot not running. Starting...
    start /min "" "D:\0\0.1\slh-telegram-bot\venv_fix\Scripts\python.exe" "D:\0\0.1\slh-telegram-bot\bot_commands.py"
    timeout /t 5 >nul
) else (
    echo [%date% %time%] Bot is running.
)

timeout /t 15 >nul
goto loop
