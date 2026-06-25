from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter

from bot.states.done_delete_task import FSMDeleteTask
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from bot.services.api_client import api_client  # 👈 Импортируем глобальный

router = Router()




@router.message(Command('delete'), StateFilter(default_state))
async def delete_task_get_id(message: Message, state: FSMContext):
    '''Удалить задачу'''
    await message.answer("Введите id задачи для её удаления")
    await state.set_state(FSMDeleteTask.is_delete)

@router.message(StateFilter(FSMDeleteTask.is_delete))
async def delete_task(message: Message, state: FSMContext):
    await api_client.delete_task(int(message.text))
    await message.answer("Задача удалена")
    await state.clear()
