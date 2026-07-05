from aiogram import Bot
from aiogram.types import BotCommand

# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command='/start',
            description='Запустить бота'
        ),
        BotCommand(
            command='/register',
            description='Регистрация'
        ),
        BotCommand(
            command='/login',
            description='Авторизация'
        ),
        BotCommand(
            command='/tasks',
            description='Список задач',
        ),
        BotCommand(
            command='/add',
            description='Добавить задачу'
        ),
        BotCommand(
            command='/correct_task',
            description='Править задачу'
        ),
        BotCommand(
            command='/cancel',
            description='Отменить действие'
        ) 

    ]
    await bot.set_my_commands(main_menu_commands)