from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from bot.keyboards.common import inline_kb_common

router = Router()

@router.callback_query(F.data == "get_home", ~StateFilter(default_state))
async def get_home(callback: CallbackQuery, state: FSMContext):
    '''Возврат домой (главное меню)'''
    await callback.answer()
    await state.clear()
    await callback.message.edit_text(
        'Привет! Я бот для управления задачами.\n'
        'Команды:\n'
        '/register — регистрация\n'
        '/login — авторизация\n'
        '/me - информация о пользователе\n',
        reply_markup=inline_kb_common
    )

@router.callback_query(F.data == "get_home", StateFilter(default_state))
async def return_home(callback: CallbackQuery, state: FSMContext):
    '''Возврат домой (главное меню)'''
    await callback.answer()
    await state.clear()
    await callback.message.edit_text(
        'Привет! Я бот для управления задачами.\n'
        'Команды:\n'
        '/register — регистрация\n'
        '/login — авторизация\n'
        '/me - информация о пользователе\n',
        reply_markup=inline_kb_common
    )
