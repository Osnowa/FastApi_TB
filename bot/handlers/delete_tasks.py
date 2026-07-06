from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter

from bot.states.done_delete_task import FSMDeleteTask
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from bot.services.api_client import api_client  # 👈 Импортируем глобальный
from bot.keyboards.common import inline_kb_common

import logging
import httpx

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data == "delete_task", StateFilter(default_state))
async def delete_task_get_id(callback: CallbackQuery, state: FSMContext):
    '''Удалить задачу (получаем id задачи )'''
    await callback.message.edit_text("Введите id задачи для её удаления", reply_markup=None)
    await state.set_state(FSMDeleteTask.is_delete)

@router.message(StateFilter(FSMDeleteTask.is_delete))
async def delete_task(message: Message, state: FSMContext, token: str):
    '''Удалить задачу'''
    try:
        await api_client.delete_task(int(message.text), token)
    except httpx.HTTPError as e:
        await message.answer(f"Произошла ошибка: {e}")
        logger.error(f"Произошла ошибка: {e}")
        return
    
    await state.clear()
    await message.edit_text("Задача удалена", reply_markup=inline_kb_common)


@router.callback_query(F.data == "delete_all_tasks")
async def delete_all_tasks(callback: CallbackQuery, token: str):
    '''Удалить все задачи пользователя'''
    try:
        await api_client.delete_all_tasks(token)
    except httpx.HTTPError as e:
        await callback.message.answer(f"Произошла ошибка: {e}")
        logger.error(f"Произошла ошибка: {e}")
        return
    await callback.message.edit_text("Все задачи удалены", reply_markup=inline_kb_common)