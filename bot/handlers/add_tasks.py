from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter

from bot.states.add_task import FSMAddTaskform
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from bot.services.api_client import api_client  # 👈 Импортируем глобальный
from bot.keyboards.add_task import kb_priority
from bot.keyboards.common import inline_kb_common

import logging
import httpx

logger = logging.getLogger(__name__)

router = Router()

@router.callback_query(F.data == "add_task" , StateFilter(default_state))
async def add_task(callback: CallbackQuery, state: FSMContext):
    '''Добавить задачу (начало)'''
    logger.info("Вошли в хендлер для добавления задачи")
    await callback.message.edit_text('Введите название задачи')
    await state.set_state(FSMAddTaskform.title)

@router.message(StateFilter(FSMAddTaskform.title))
async def add_task_description(message: Message, state: FSMContext):
    '''Добавить описание задачи'''
    await state.update_data(title=message.text)
    await message.answer('Введите описание задачи')
    await state.set_state(FSMAddTaskform.description)

@router.message(StateFilter(FSMAddTaskform.description))
async def add_task_priority(message: Message, state: FSMContext):
    '''Добавить приоритет задачи'''
    await state.update_data(description=message.text)
    await message.answer('Выберите приоритет задачи', reply_markup = kb_priority)
    await state.set_state(FSMAddTaskform.priority)

@router.callback_query(F.data.in_(['low', 'medium', 'high', 'noy']) , StateFilter(FSMAddTaskform.priority))
async def add_task_finish(callback: CallbackQuery, state: FSMContext, token: str):
    '''Добавить задачу'''
    request_user = callback.data

    await state.update_data(priority = request_user)
    data = await state.get_data()
    try:
        response = await api_client.create_task(data['title'], data['description'], data['priority'], token)
    except httpx.HTTPError as e:
        await callback.message.answer(f"Произошла ошибка: {e}")
        logger.error(f"Произошла ошибка: {e}")
        return

    await state.clear()
    await callback.message.edit_text(f"Задача <b>{response['title']}</b> добавлена", reply_markup = inline_kb_common)