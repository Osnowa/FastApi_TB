from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import httpx
import logging

from bot.services.api_client import api_client  # 👈 Импортируем глобальный

router = Router()
logger = logging.getLogger(__name__)

@router.message(Command('tasks'))
async def get_tasks(message: Message):
    '''Получить все задачи'''
    try:
        response = await api_client.get_tasks() # Получаем списко задач
    except httpx.HTTPError as e:
        await message.answer(f"Произошла ошибка: {e}")
        logger.error(f"Произошла ошибка: {e}")
        return
    
    if response is None:
        await message.answer("Задач нет")
    
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
    await message.answer(text)
