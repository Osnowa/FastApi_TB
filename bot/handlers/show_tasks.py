from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.services.api_client import api_client  # 👈 Импортируем глобальный

router = Router()


@router.message(Command('tasks'))
async def get_tasks(message: Message):
    '''Получить все задачи'''
    response = await api_client.get_tasks() # Получаем списко задач
    if response is None:
        await message.answer("Задач нет")
    
    text = "Список задач:\n\n"
    for task in response:
        text += (
            f"ID: {task['id']}\n"
            f"Название: {task['title']}\n"
            f"Описание: {task['description']}\n"
            f"Статус: {task['status']}\n"
            f"Приоритет: {task['priority'] or '-'}\n\n"
        )
    await message.answer(text)
