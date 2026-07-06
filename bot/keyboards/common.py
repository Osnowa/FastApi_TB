from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.keyboards.common_bytton import bytton_home

# bytton_register = InlineKeyboardButton(text="Регистрация", callback_data="register")
# bytton_login = InlineKeyboardButton(text="Вход", callback_data="login")
bytton_tasks = InlineKeyboardButton(text="Задачи", callback_data="get_tasks")
bytton_add_task = InlineKeyboardButton(text="Добавить задачу", callback_data="add_task")
bytton_correct_task = InlineKeyboardButton(text="Корректировать", callback_data="correct_task")

inline_kb_common = InlineKeyboardMarkup(
    inline_keyboard=[[bytton_tasks, bytton_add_task], [bytton_correct_task], [bytton_home]]
)