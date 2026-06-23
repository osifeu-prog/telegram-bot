from aiogram import Router, types
from aiogram.filters import Command
from src.bot.db.database import AsyncSessionLocal
from src.bot.db.models import User, Contact
from sqlalchemy import select, func
import uuid, csv, io, re

router = Router()

@router.message(Command("start"))
async def start_cmd(message: types.Message):
    kb = types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="🏠 Home"), types.KeyboardButton(text="📊 Stats")],
        [types.KeyboardButton(text="🛒 Shop"), types.KeyboardButton(text="💼 Wallet")],
        [types.KeyboardButton(text="🗳 Vote"), types.KeyboardButton(text="📋 Tasks")],
    ], resize_keyboard=True)
    await message.answer("Welcome! Choose an option:", reply_markup=kb)

# ---------- PARTNER ----------
@router.message(Command("partner_register"))
async def partner_register_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()
        if not user:
            await message.answer("You must /start first.")
            return
        try:
            _ = user.partner_code
        except AttributeError:
            await message.answer("System update in progress. Try again in a minute.")
            return
        if user.partner_code:
            await message.answer(f"You are already a partner! Code: `{user.partner_code}`")
            return
        user.partner_code = uuid.uuid4().hex[:8]
        session.add(user)
        await session.commit()
    bot_username = (await message.bot.get_me()).username
    ref_link = f"https://t.me/{bot_username}?start=ref_{message.from_user.id}"
    await message.answer(
        f"🎉 You are now a partner!\n"
        f"Your referral link: {ref_link}\n"
        f"Commission: {user.partner_commission}%\n"
        f"Share it to earn!"
    )

@router.message(Command("partner_stats"))
async def partner_stats_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, message.from_user.id)
        if not user or not getattr(user, 'partner_code', None):
            await message.answer("You are not a partner yet. Use /partner_register.")
            return
        result = await session.execute(
            select(func.count(User.telegram_id)).where(User.referrer_id == message.from_user.id)
        )
        referral_count = result.scalar()
    await message.answer(
        f"📊 **Partner Stats**\n"
        f"Referrals: {referral_count}\n"
        f"Commission rate: {user.partner_commission}%\n"
        f"Your code: `{user.partner_code}`"
    )

# ---------- TASKS ----------
@router.message(Command("tasks"))
async def tasks_cmd(message: types.Message):
    tasks_list = [
        "✅ MVP 100%  daily loop, wallet, shop, mini-app",
        "✅ V1 95%  KYC, referral, governance, groups, i18n, broadcast",
        "✅ V2 92%  achievements, AI, menu, progress, teaser, leaderboard",
        "✅ Notifications  mute/unmute, random daily reveal",
        "✅ Voting system  propose, vote, governance dashboard",
        "✅ Contacts  CSV upload, phone list import",
        "✅ Partner system  15% commission, partner links",
        "⏳ Bulk messaging  send to contacts/groups",
        "⏳ Payments  Telegram Stars / USDT integration",
        "⏳ Onboarding flow  welcome messages, tutorial",
        "⏳ Final testing & launch prep",
    ]
    await message.answer("📋 **Project Task List**\n" + "\n".join(tasks_list))

# ---------- CONTACTS ----------
@router.message(Command("upload_contacts"))
async def upload_contacts_cmd(message: types.Message):
    await message.answer(
        "📎 Please send a CSV or VCF file.\n\n"
        "CSV columns: phone,name,group\n"
        "VCF (vCard): phone numbers and names will be extracted."
    )

@router.message(Command("contacts_list"))
async def contacts_list_cmd(message: types.Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Contact).where(Contact.owner_id == message.from_user.id).limit(50)
        )
        contacts = result.scalars().all()
    if not contacts:
        await message.answer("No contacts found. Upload a CSV/VCF with /upload_contacts.")
        return
    lines = ["📋 **Your Contacts**"]
    for c in contacts:
        lines.append(f"{c.phone}  {c.name or 'N/A'} [{c.group_name or '-'}]")
    await message.answer('\n'.join(lines))

@router.message(Command("import_phones"))
async def import_phones_cmd(message: types.Message):
    text = message.text.removeprefix("/import_phones ").strip()
    if not text:
        await message.answer("📝 Usage: /import_phones <list of numbers>")
        return
    phones = re.split(r'[,\n\s]+', text)
    phones = [p.strip() for p in phones if p.strip()]
    if not phones:
        await message.answer("No valid phone numbers found.")
        return
    count = 0
    async with AsyncSessionLocal() as session:
        for phone in phones:
            if (phone.startswith('+') or phone.startswith('0')) and len(phone) >= 9:
                contact = Contact(owner_id=message.from_user.id, phone=phone, name=None, group_name=None)
                session.add(contact)
                count += 1
        await session.commit()
    await message.answer(f"✅ Imported {count} phone numbers.")

@router.message(lambda msg: msg.document is not None)
async def handle_file(message: types.Message):
    doc = message.document
    file_name = doc.file_name.lower()
    if not (file_name.endswith('.csv') or file_name.endswith('.vcf')):
        await message.answer("❌ Only CSV or VCF files accepted.")
        return
    file = await message.bot.get_file(doc.file_id)
    content = await message.bot.download_file(file.file_path)
    raw = content.read().decode('utf-8-sig')
    count = 0
    async with AsyncSessionLocal() as session:
        if file_name.endswith('.csv'):
            reader = csv.DictReader(io.StringIO(raw))
            for row in reader:
                phone = row.get('phone', '').strip()
                if not phone:
                    continue
                name = row.get('name', '').strip()
                group = row.get('group', '').strip()
                contact = Contact(owner_id=message.from_user.id, phone=phone, name=name, group_name=group)
                session.add(contact)
                count += 1
        elif file_name.endswith('.vcf'):
            entries = raw.split('BEGIN:VCARD')
            for entry in entries:
                if 'END:VCARD' not in entry:
                    continue
                tel_match = re.search(r'TEL[^:]*:([^\r\n]+)', entry)
                if not tel_match:
                    continue
                phone = tel_match.group(1).strip()
                phone = re.sub(r'[^\d+]', '', phone)
                if not phone:
                    continue
                name_match = re.search(r'FN[^:]*:([^\r\n]+)', entry)
                name = name_match.group(1).strip() if name_match else None
                contact = Contact(owner_id=message.from_user.id, phone=phone, name=name, group_name=None)
                session.add(contact)
                count += 1
        await session.commit()
    await message.answer(f"✅ Uploaded {count} contacts from {file_name}.")
