from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardRemove

from middleware.auth import auth

router = Router()

@router.message(F.text == "Как дела?")
@auth
async def how_are_u_handler(message: types.Message):
    await message.answer(f"У меня все прекрасно, а у тебя что нового?")
