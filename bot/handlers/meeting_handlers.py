from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardRemove

from database.connection import AsyncSessionLocal
import database.methods

from aiogram.fsm.context import FSMContext
from middleware.auth import auth
from states.meeting_states import MeetingNewUser

from keyboards import start_kb

router = Router()

@router.message(CommandStart())
@router.message(F.text == "Познакомиться")
async def start_handler(message: types.Message, state: FSMContext):
    await state.set_state(MeetingNewUser.name)
    await message.answer(f"Привет! Меня зовут Ая, а как тебя зовут?", reply_markup=ReplyKeyboardRemove())

@router.message(MeetingNewUser.name)
async def name_handler(message: types.Message, state: FSMContext):
    name = message.text.strip().lower()
    await state.update_data(name=name)
    await state.set_state(MeetingNewUser.diminutive_affectionate)
    await message.answer(f"Приятно познакомиться {name.capitalize()}! А как я могу лаского тебя называть? Только давай через запятую, чтобы я потом не запуталась.")

@router.message(MeetingNewUser.diminutive_affectionate)
async def diminutive_affectionate_handler(message: types.Message, state: FSMContext):
    message_text = message.text.strip().lower()
    if message_text != "никак":
        if ',' in message_text:
            diminutive_affectionate = [item.strip() for item in message_text.split(',')]
            await message.answer(f"Ого, как много!")
        else:
            diminutive_affectionate = [message_text]
            await message.answer(f"Я запомню :)")
    else:
        diminutive_affectionate = None
        await message.answer(f"Ой, ну и ладно :(")

    await state.update_data(diminutive_affectionate=diminutive_affectionate)
    await state.set_state(MeetingNewUser.timezone)
    await message.answer(f"А в какой временной зоне ты живешь?", reply_markup=await start_kb.meeting_timezone_keyboard())


@router.callback_query(F.data.startswith("selectedtimezone_"))
async def handle_selected_timezone_callback(callback_query: types.CallbackQuery, state: FSMContext):
    timezone = callback_query.data.split("_")[1]
    await state.update_data(timezone=timezone)

    await callback_query.message.answer("А по какому рабочему графику ты живешь?", reply_markup=await start_kb.meeting_weektype_keyboard())
    await callback_query.answer()

@router.callback_query(F.data.startswith("selectedweektype_"))
async def handle_selected_weektype_callback(callback_query: types.CallbackQuery, state: FSMContext):
    weektype = callback_query.data.split("_")[1]
    await state.update_data(weektype=weektype)
    await callback_query.message.answer("Вот и познакомились, ура ура :3")
    data = await state.get_data()
    await callback_query.answer()

    async with AsyncSessionLocal() as session:
        await database.methods.update_user(
            session=session,
            telegram_id=callback_query.from_user.id,
            username=callback_query.from_user.username,
            name=data['name'],
            timezone_id=data['timezone'],
            weektype_id=data['weektype'],
            diminutive_affectionate_list=data['diminutive_affectionate']
        )

    await state.clear()

@auth
@router.message(F.text == "Забудь меня")
async def forgive_me_handler(message: types.Message):
    async with AsyncSessionLocal() as session:
        await database.methods.delete_user(session, message.from_user.id)
    await message.answer("Я никогда тебя не забуду! Но так уж и быть, сделаю вид что не помню 😜")