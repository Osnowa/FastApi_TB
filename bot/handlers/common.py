from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from bot.keyboards.common import inline_kb_common

import logging

logger = logging.getLogger(__name__)

router = Router()

@router.message(Command('start'))
async def start(message: Message):
    await message.answer('Привет! Я бот для управления задачами.\n'
                         'Команды:\n'
                         '/register — регистрация\n'
                         '/login — авторизация\n'
                         '/me - информация о пользователе\n',
                         reply_markup = inline_kb_common
                         )
    
@router.message(Command('cancel'), ~StateFilter(default_state))
async def cancel(message: Message, state: FSMContext):
    '''Отменить действие'''
    logger.info("Вошли в хендлер для отмены действия")
    await message.answer('Действие отменено')
    await state.clear()


    