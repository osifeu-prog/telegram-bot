import os
from io import BytesIO
from aiogram import Router, F, types
from aiogram.filters import Command
import httpx
from PyPDF2 import PdfReader

router = Router()
ADMIN_ID = 8789977826

def is_admin(msg: types.Message) -> bool:
    return msg.from_user.id == ADMIN_ID

@router.message(Command("analyze_pdf"))
async def analyze_pdf_help(message: types.Message):
    """הוראות שימוש"""
    await message.reply(
        "📄 **Analyze PDF with AI**\n\n"
        "1️⃣ Send me a PDF file (as a document).\n"
        "2️⃣ Add a caption with your question/instruction.\n"
        "3️⃣ I'll extract the text and ask the AI to analyze it.\n\n"
        "Example: Send a PDF with the caption 'Summarize this contract'"
    )

@router.message(F.document)
async def handle_pdf(message: types.Message):
    """Extract text from PDF and send to AI"""
    if not message.document.file_name.endswith('.pdf'):
        await message.reply("❌ Only PDF files are supported.")
        return
    
    await message.reply("📄 Reading PDF...")
    
    # Download the file
    file = await message.bot.get_file(message.document.file_id)
    file_bytes = await message.bot.download_file(file.file_path)
    
    # Extract text
    try:
        pdf = PdfReader(BytesIO(file_bytes.read()))
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        await message.reply(f"❌ Failed to read PDF: {e}")
        return
    
    # Get user's question (caption or default)
    question = message.caption or "Summarize this document"
    
    # Send to AI
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        await message.reply("❌ GROQ_API_KEY not set.")
        return
    
    await message.reply("🤔 Analyzing with AI...")
    
    # Truncate text to fit context window
    max_chars = 30000
    if len(text) > max_chars:
        text = text[:max_chars] + "\n... (truncated)"
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {"role": "system", "content": "You are a document analysis assistant. Analyze the following PDF text and answer the user's question."},
                        {"role": "user", "content": f"Question: {question}\n\nPDF Content:\n{text}"}
                    ],
                    "max_tokens": 1000
                },
                timeout=60
            )
            data = resp.json()
            reply = data["choices"][0]["message"]["content"]
            await message.reply(f"🤖 **AI Analysis:**\n\n{reply}")
        except Exception as e:
            await message.reply(f"❌ AI Error: {e}")
