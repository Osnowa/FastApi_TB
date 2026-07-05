from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_continue = InlineKeyboardButton(text="Продолжить", callback_data="continue")

kb_continue = InlineKeyboardMarkup(
    inline_keyboard=[[button_continue]]
)

button_low = InlineKeyboardButton(text="Низкий", callback_data="low")
button_medium = InlineKeyboardButton(text="Средний", callback_data="medium")
button_high = InlineKeyboardButton(text="Высокий", callback_data="high")
button_none = InlineKeyboardButton(text="Нет", callback_data="none")

kb_priority = InlineKeyboardMarkup(
    inline_keyboard=[[button_low, button_medium, button_high], [button_none]]
)