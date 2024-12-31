from functools import wraps
from aiogram import types
from database.connection import AsyncSessionLocal
from database.methods import user_exist
from config import ADMIN_ID

from keyboards import start_kb

def auth(handler):
    @wraps(handler)
    async def wrapper(event: types.Message, *args, **kwargs):
        async with AsyncSessionLocal() as session:
            try:
                user_exists = await user_exist(session, event.from_user.id)

                if not user_exists:
                    await event.answer(f"Мы с тобой еще не знакомы, давай познакомимся?", reply_markup=start_kb.meeting_start)
                    return
                
                return await handler(event, *args, **kwargs)

            finally:
                await session.close()

    return wrapper

def admin_required(handler):
    @wraps(handler)
    async def wrapper(event: types.Message, *args, **kwargs):
        try:
            if event.from_user.id != ADMIN_ID:
                await event.answer(f"Я не буду тебя слушать, мы еще не на столько близки.")
                return
            
            return await handler(event, *args, **kwargs)

        finally:
            pass

    return wrapper