from aiogram import Router, types

router = Router()

@router.message()
async def echo_all(message: types.Message):
    await message.answer(f"ECHO: {message.text}")
