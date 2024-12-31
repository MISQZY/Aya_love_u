from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.methods import get_timezones, get_weektypes
from database.connection import AsyncSessionLocal


meeting_start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Познакомиться")]
],
one_time_keyboard=True, resize_keyboard=True)


async def meeting_timezone_keyboard():
    #timezones = [{'id': 1, "name": "GMT+1"},{'id': 2, "name": "GMT+2"},{'id': 3, "name": "GMT+3"}]
    async with AsyncSessionLocal() as session:
        timezones = await get_timezones(session)

    keyboard = InlineKeyboardBuilder()
    for timezone in timezones:
        keyboard.add(InlineKeyboardButton(text=timezone['name'], callback_data=f"selectedtimezone_{timezone['id']}"))
    return keyboard.adjust(1).as_markup()


async def meeting_weektype_keyboard():
    #weektypes = [{'id': 1, "name": "5/2"},{'id': 2, "name": "2/2"},{'id': 3, "name": "Другой"}]
    async with AsyncSessionLocal() as session:
        weektypes = await get_weektypes(session)

    keyboard = InlineKeyboardBuilder()
    for weektype in weektypes:
        keyboard.add(InlineKeyboardButton(text=weektype['name'], callback_data=f"selectedweektype_{weektype['id']}"))
    return keyboard.adjust(1).as_markup()