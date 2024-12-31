from aiogram import types, Router, F

from middleware.auth import admin_required
from main import update_routes

router = Router()


@router.message(F.text == "Обновись")
@admin_required
async def reload_routes_handler(message: types.Message):
    try:
        await message.answer("Я успешно обновилась!")
    except Exception as e:
        await message.answer(f"У меня не получилось обновиться :( Ошибочка: {e}")