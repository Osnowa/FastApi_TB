from aiogram.fsm.state import StatesGroup, State

class FSMAddRegister(StatesGroup):
    email = State()
    password = State()

class FSMAddLogin(StatesGroup):
    email = State()
    password = State()
