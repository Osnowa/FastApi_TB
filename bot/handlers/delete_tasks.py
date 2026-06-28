from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter

from bot.states.done_delete_task import FSMDeleteTask
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from bot.services.api_client import api_client  # 👈 Импортируем глобальный

import logging
import httpx

logger = logging.getLogger(__name__)

router = Router()




@router.message(Command('delete'), StateFilter(default_state))
async def delete_task_get_id(message: Message, state: FSMContext):
    '''Удалить задачу (получаем id задачи )'''
    logger.info("Вошли в хендлер для удаления задачи - получаем id задачи")
    await message.answer("Введите id задачи для её удаления")
    await state.set_state(FSMDeleteTask.is_delete)

@router.message(StateFilter(FSMDeleteTask.is_delete))
async def delete_task(message: Message, state: FSMContext):
    '''Удалить задачу'''
    try:
        await api_client.delete_task(int(message.text))
    except httpx.HTTPError as e:
        await message.answer(f"Произошла ошибка: {e}")
        logger.error(f"Произошла ошибка: {e}")
        return
    await message.answer("Задача удалена")
    await state.clear()
