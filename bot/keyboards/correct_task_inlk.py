from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.keyboards.common_bytton import bytton_home

button_delete = InlineKeyboardButton(text="Удалить", callback_data="delete_task")
button_delete_all = InlineKeyboardButton(text="Удалить все", callback_data="delete_all_tasks")
button_done = InlineKeyboardButton(text="Отметить done", callback_data="done_task")


inline_kb_correct_task = InlineKeyboardMarkup(
    inline_keyboard=[[button_delete, button_delete_all], [button_done], [bytton_home]]
)