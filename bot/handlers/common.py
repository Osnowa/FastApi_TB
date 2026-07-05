from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

import logging

logger = logging.getLogger(__name__)

router = Router()

@router.message(Command('start'))
async def start(message: Message):
    await message.answer('Привет! Я бот для управления задачами.\n'
                         'Команды:\n'
                         '/register — регистрация\n'
                         '/login — авторизация\n'
                         '/tasks — список задач\n'
                         '/add — добавить задачу\n'
                         '/correct_task — править задачу\n'
                         )
    
@router.message(Command('cancel'), ~StateFilter(default_state))
async def cancel(message: Message, state: FSMContext):
    '''Отменить действие'''
    logger.info("Вошли в хендлер для отмены действия")
    await message.answer('Действие отменено')
    await state.clear()