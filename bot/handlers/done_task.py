from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter

from bot.states.done_delete_task import FSMDoneTask
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from bot.services.api_client import api_client  # 👈 Импортируем глобальный
import logging
import httpx

logger = logging.getLogger(__name__)

router = Router()



@router.callback_query(F.data == "done_task", StateFilter(default_state))
async def done_task_get_id(callback: CallbackQuery, state: FSMContext):
    '''Отметить задачу выполненной (получаем id задачи )'''
    logger.info("Вошли в хендлер для отметки задачи выполненной для получнения id задачи")
    await callback.message.edit_text(text = "Введите id задачи для её выполнения", reply_markup=None)
    await state.set_state(FSMDoneTask.is_done)

@router.message(StateFilter(FSMDoneTask.is_done))
async def done_task(message: Message, state: FSMContext, token: str):
    '''Отметить задачу выполненной'''
    try:
        await api_client.patch_task(int(message.text), {"status": "done"}, token)
    except httpx.HTTPError as e:
        await message.answer(f"Произошла ошибка: {e}")
        logger.error(f"Произошла ошибка: {e}")
        return
    await message.answer("Задача помечана как выполнененная")
    await state.clear()