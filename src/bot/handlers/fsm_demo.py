from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.bot.states.user_states import UserForm

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
    data = await state.update_data(age=message.text)
    await message.answer(f"נעים להכיר {data['name']}, בן {data['age']}!")
    await state.clear()
