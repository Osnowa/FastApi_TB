from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter

from bot.states.add_task import FSMAddTaskform
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from bot.services.api_client import api_client  # 👈 Импортируем глобальный

router = Router()

@router.message(Command('add'), StateFilter(default_state))
async def add_task(message: Message, state: FSMContext):
    '''Добавить задачу (начало)'''
    await message.answer('Введите название задачи')
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
    await message.answer('Введите приоритет задачи, либо введите нет - если нет приоритета')
    await state.set_state(FSMAddTaskform.priority)

@router.message(StateFilter(FSMAddTaskform.priority))
async def add_task_finish(message: Message, state: FSMContext):
    '''Добавить задачу'''
    request_user = message.text
    if message.text == 'нет':
        request_user = None
    if request_user in ['low', 'medium', 'high', None]:
        await state.update_data(priority = request_user)
        data = await state.get_data()
        response = await api_client.create_task(data['title'], data['description'], data['priority'])
    else:
        await message.answer("Неверный приоритет задачи")
        return
    await message.answer(f"Задача {response['title']} добавлена")
    await state.clear()