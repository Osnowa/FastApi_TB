from aiogram import F, Router
from aiogram.types import CallbackQuery
import httpx
import logging

from bot.services.api_client import api_client  # 👈 Импортируем глобальный

router = Router()
logger = logging.getLogger(__name__)

@router.callback_query(F.data == "get_tasks")
async def get_tasks(callback: CallbackQuery, token: str):
    '''Получить все задачи'''
    try:
        response = await api_client.get_tasks(token) # Получаем списко задач
    except httpx.HTTPError as e:
        await callback.message.answer(f"Произошла ошибка: {e}")
        logger.error(f"Произошла ошибка: {e}")
        return
    
    if response is None:
        await callback.message.edit_text("Задач нет", reply_markup=callback.message.reply_markup)
    
    text = "Список задач:\n\n"
    for task in response:
        text += (
            f"ID: {task['id']}\n"
            f"Название: {task['title']}\n"
            f"Описание: {task['description']}\n"
            f"Статус: {task['status']}\n"
            f"Приоритет: {task['priority'] or '-'}\n"
            f"Время добавления задачи: {task['created_at']}\n\n"
        )
    await callback.message.edit_text(text, reply_markup=callback.message.reply_markup)
