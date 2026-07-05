from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# bytton_register = InlineKeyboardButton(text="Регистрация", callback_data="register")
# bytton_login = InlineKeyboardButton(text="Вход", callback_data="login")
bytton_tasks = InlineKeyboardButton(text="Задачи", callback_data="get_tasks")
bytton_add_task = InlineKeyboardButton(text="Добавить задачу", callback_data="add_task")
bytton_correct_task = InlineKeyboardButton(text="Корректировать задачу", callback_data="correct_task")

inline_kb_common = InlineKeyboardMarkup(
    inline_keyboard=[[bytton_tasks, bytton_add_task], [bytton_correct_task]]
)