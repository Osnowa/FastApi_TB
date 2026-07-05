from aiogram import F, Router
from aiogram.types import CallbackQuery
from bot.keyboards.correct_task_inlk import inline_kb_correct_task

router = Router()

@router.callback_query(F.data == "correct_task")
async def correct_task(callback: CallbackQuery):
    await callback.message.edit_text('Добрый день, пожалуйста, выбери что Вы хотите сделать с задачей',
                         reply_markup=inline_kb_correct_task)