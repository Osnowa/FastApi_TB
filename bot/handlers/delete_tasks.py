from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter

from bot.states.done_delete_task import FSMDeleteTask
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from bot.services.api_client import api_client  # 👈 Импортируем глобальный


import logging
import httpx

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data == "delete_task", StateFilter(default_state))
async def delete_task_get_id(callback: CallbackQuery, state: FSMContext):
    '''Удалить задачу (получаем id задачи )'''
    await callback.message.edit_reply_markup("Введите id задачи для её удаления", reply_markup=None)
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
    await message.answer("Задача удалена")
    await state.clear()
