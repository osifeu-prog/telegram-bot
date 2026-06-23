import csv, io, json
from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select, func
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import Contact

router = Router()

@router.message(Command("upload_contacts"))
async def upload_contacts_cmd(message: types.Message):
    await message.answer(
        "📎 Please send a CSV file with columns: phone,name,group (name and group optional).\n"
        "Example:\n"
        "phone,name,group\n"
        "+972501234567,John,partners\n"
        "+972502345678,Jane,clients"
    )

@router.message(lambda msg: msg.document is not None)
async def handle_csv(message: types.Message):
    doc = message.document
    if not doc.file_name.endswith('.csv'):
        await message.answer("❌ Only CSV files accepted.")
        return
    # Download file
    file = await message.bot.get_file(doc.file_id)
    content = await message.bot.download_file(file.file_path)
    text = content.read().decode('utf-8-sig')
    reader = csv.DictReader(io.StringIO(text))
    count = 0
    async with AsyncSessionLocal() as session:
        for row in reader:
            phone = row.get('phone', '').strip()
            if not phone:
                continue
            name = row.get('name', '').strip()
            group = row.get('group', '').strip()
            contact = Contact(
                owner_id=message.from_user.id,
                phone=phone,
                name=name,
                group_name=group
            )
            session.add(contact)
            count += 1
        await session.commit()
    await message.answer(f"✅ Uploaded {count} contacts.")


@router.message(Command("import_phones"))
async def import_phones_cmd(message: types.Message):
    """Import phone numbers from a pasted list (one per line, or comma separated)."""
    text = message.text.removeprefix("/import_phones ").strip()
    if not text:
        await message.answer("📝 Usage: /import_phones <list of numbers>\nExample: /import_phones +972501234567, +972502345678")
        return
    # Split by comma, newline, or whitespace
    import re
    phones = re.split(r'[,\n\s]+', text)
    phones = [p.strip() for p in phones if p.strip()]
    if not phones:
        await message.answer("No valid phone numbers found.")
        return
    count = 0
    async with AsyncSessionLocal() as session:
        for phone in phones:
            # Basic validation: starts with + or 0, length >= 9
            if (phone.startswith('+') or phone.startswith('0')) and len(phone) >= 9:
                contact = Contact(
                    owner_id=message.from_user.id,
                    phone=phone,
                    name=None,
                    group_name=None
                )
                session.add(contact)
                count += 1
        await session.commit()
    await message.answer(f"✅ Imported {count} phone numbers.")

@router.message(Command("contacts_list"))
async def contacts_list_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Contact).where(Contact.owner_id == message.from_user.id).limit(50)
        )
        contacts = result.scalars().all()
    if not contacts:
        await message.answer("No contacts found. Upload a CSV with /upload_contacts.")
        return
    lines = ["📋 **Your Contacts**"]
    for c in contacts:
        lines.append(f"{c.phone}  {c.name or 'N/A'} [{c.group_name or '-'}]")
    await message.answer('\n'.join(lines))

