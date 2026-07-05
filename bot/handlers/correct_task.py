from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.keyboards.correct_task_inlk import inline_kb_correct_task
router = Router()

@router.message(Command('correct_task'))
async def correct_task(message: Message):
    await message.answer('Добрый день, пожалуйста, выбери что Вы хотите сделать с задачей',
                         reply_markup=inline_kb_correct_task)