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
            command='/cancel',
            description='Отменить действие'
        ),
        BotCommand(
            command='/me',
            description='Информация о пользователе'
        ) 

    ]
    await bot.set_my_commands(main_menu_commands)