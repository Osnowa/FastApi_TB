from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_delete = InlineKeyboardButton(text="Удалить", callback_data="delete_task")
button_done = InlineKeyboardButton(text="Отметить выполненной", callback_data="done_task")


inline_kb_correct_task = InlineKeyboardMarkup(
    inline_keyboard=[[button_delete, button_done]]
)