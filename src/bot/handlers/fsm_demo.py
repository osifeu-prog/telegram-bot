from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.bot.states.user_states import UserForm
from src.bot.db.database import AsyncSessionLocal
from src.bot.models.user import User

router = Router()

@router.message(Command("form"))
async def start_form(message: types.Message, state: FSMContext):
    await message.answer("מה השם שלך?")
    await state.set_state(UserForm.name)

@router.message(UserForm.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("בן כמה אתה?")
    await state.set_state(UserForm.age)

@router.message(UserForm.age)
async def get_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("מה האימייל שלך?")
    await state.set_state(UserForm.email)

@router.message(UserForm.email)
async def get_email(message: types.Message, state: FSMContext):
    data = await state.update_data(email=message.text)

    async with AsyncSessionLocal() as session:
        user = User(
            telegram_id=message.from_user.id,
            name=data["name"],
            age=data["age"],
            email=data["email"],
        )
        session.add(user)
        await session.commit()

    await message.answer(
        f"סיכום:\n"
        f"שם: {data['name']}\n"
        f"גיל: {data['age']}\n"
        f"אימייל: {data['email']}\n"
        f"הנתונים נשמרו במערכת. תודה!"
    )
    await state.clear()




