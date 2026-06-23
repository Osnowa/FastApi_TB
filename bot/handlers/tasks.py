from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter

from bot.states.add_task import FSMAddTaskform
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
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
        text += f"{task['title']}: \n {task['description']}\n\n"

    await message.answer(text)


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
    await message.answer('Введите приоритет задачи, либо оставьте поле пустым')
    await state.set_state(FSMAddTaskform.priority)

@router.message(StateFilter(FSMAddTaskform.priority))
async def add_task_priority(message: Message, state: FSMContext):
    '''Добавить задачу'''
    await state.update_data(priority=message.text)
    data = await state.get_data()
    response = await api_client.create_task(data['title'], data['description'], data['priority'])
    await message.answer(f"Задача {response['title']} добавлена")
    await state.clear()

@router.message(Command('delete'))
async def delete_task(message: Message, id_task: int):
    '''Удалить задачу'''
    await message.answer("Введите id задачи для удаления")
    response = await api_client.delete_task(id_task)
    if response:
        await message.answer(f"Задача {id_task} удалена")
    else:
        await message.answer(f"Задача {id_task} не найдена")

@router.message(Command('done'))
async def done_task(message: Message, id_task: int):
    '''Отметить задачу выполненной'''
    await message.answer("Введите id задачи для того, что бы отметить её выполненной")
    response = await api_client.patch_task(id_task, {"status": "done"})
    if response:
        await message.answer(f"Задача {id_task} выполнена")
    else:
        await message.answer(f"Задача {id_task} не найдена")