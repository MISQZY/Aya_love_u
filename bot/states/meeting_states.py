from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup

class MeetingNewUser(StatesGroup):
    name = State()
    diminutive_affectionate = State()
    timezone = State()
    weektype = State()
