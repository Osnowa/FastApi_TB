from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

router = Router()

@router.message(Command('start'))
async def start(message: Message):
    await message.answer('Привет! Я бот для управления задачами.\n'
                         'Команды:\n'
                         '/tasks — список задач\n'
                         '/add — добавить задачу\n'
                         '/done — отметить задачу выполненной\n'
                         '/delete — удалить задачу\n'
                         )
    
@router.message(Command('cancel'), ~StateFilter(default_state))
async def cancel(message: Message, state: FSMContext):
    '''Отменить действие'''
    await message.answer('Действие отменено')
    await state.clear()