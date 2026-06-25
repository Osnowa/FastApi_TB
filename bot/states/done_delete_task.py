from aiogram.fsm.state import StatesGroup, State


class FSMDoneTask(StatesGroup):
    is_done = State()

class FSMDeleteTask(StatesGroup):
    is_delete = State()