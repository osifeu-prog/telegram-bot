import os, subprocess, httpx
from datetime import datetime
from aiogram import Router, types
from aiogram.filters import Command

router = Router()
ADMIN_ID = 8789977826

def is_admin(msg: types.Message) -> bool:
    return msg.from_user.id == ADMIN_ID

@router.message(Command("backup"))
async def backup_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    await message.answer("🔄 Creating backup...")
    try:
        timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        filename = f"backups/slh-bot-backup-{timestamp}.zip"
        subprocess.run(
            f"zip -r {filename} src static locales requirements.txt railway.json -x '*__pycache__*'",
            shell=True, cwd="/app", check=True
        )
        subprocess.run("git add backups/ && git commit -m 'Auto backup' && git push", shell=True, cwd="/app")
        await message.answer(f"✅ Backup created: {filename}")
    except Exception as e:
        await message.answer(f"❌ Backup failed: {e}")

@router.message(Command("ask_ai"))
async def ask_ai_cmd(message: types.Message):
    if not is_admin(message):
        await message.answer("⛔ Access denied.")
        return
    prompt = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else ""
    if not prompt:
        await message.answer("Usage: /ask_ai <your prompt>")
        return
    
    await message.answer("🤔 Thinking...")
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        await message.answer("❌ GROQ_API_KEY not set.")
        return
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {"role": "system", "content": "You are a helpful bot assistant. Answer in the language the user asks."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 500
                },
                timeout=30
            )
            data = resp.json()
            reply = data["choices"][0]["message"]["content"]
            await message.answer(f"🤖 **AI Response:**\n\n{reply}")
        except Exception as e:
            await message.answer(f"❌ AI Error: {e}")


