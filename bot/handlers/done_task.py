from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter

from bot.states.done_delete_task import FSMDoneTask
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from bot.services.api_client import api_client  # 👈 Импортируем глобальный

router = Router()



@router.message(Command('done'), StateFilter(default_state))
async def done_task_get_id(message: Message, state: FSMContext):
    await message.answer("Введите id задачи для её выполнения")
    await state.set_state(FSMDoneTask.is_done)

@router.message(StateFilter(FSMDoneTask.is_done))
async def done_task(message: Message, state: FSMContext):
    await api_client.patch_task(int(message.text), {"status": "done"})
    await message.answer("Задача помечана как выполнененная")
    await state.clear()