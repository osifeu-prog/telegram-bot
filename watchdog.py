import subprocess
import time
import sys

print("SLH Bot Watchdog started...")

while True:
    try:
        # בדוק אם bot_commands.py כבר רץ
        result = subprocess.run(['tasklist', '/fi', 'imagename eq python.exe'], 
                              capture_output=True, text=True, shell=True)
        if 'bot_commands.py' not in result.stdout:
            print(f"[{time.strftime('%H:%M:%S')}] Bot not found. Restarting...")
            subprocess.Popen([
                r"D:\0\0.1\slh-telegram-bot\venv_fix\Scripts\python.exe",
                r"D:\0\0.1\slh-telegram-bot\bot_commands.py"
            ])
        else:
            print(f"[{time.strftime('%H:%M:%S')}] Bot is alive.")
    except Exception as e:
        print("Watchdog error:", e)
    
    time.sleep(15)
