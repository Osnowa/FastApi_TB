from aiogram.fsm.state import StatesGroup, State

class FSMAddTaskform(StatesGroup):
    title = State()
    description = State()
    priority = State()