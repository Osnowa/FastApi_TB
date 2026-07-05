import logging

import asyncio
from aiogram import Bot, Dispatcher
from bot.config import BotConfig
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from bot.handlers.add_tasks import router as router_add_tasks
from bot.handlers.delete_tasks import router as router_delete_tasks
from bot.handlers.done_task import router as router_done_tasks
from bot.handlers.show_tasks import router as router_show_tasks
from bot.handlers.common import router as router_common
from bot.handlers.auth import router as router_auth
from bot.handlers.correct_task import router as router_correct_task

from bot.middleware.auth_middleware import Token_Middleware

from bot.keyboards.set_menu import set_main_menu

from aiogram.fsm.storage.redis import RedisStorage
from bot.states.redis import r

from bot.services.api_client import api_client  # 👈 Импортируем глобальный

logger = logging.getLogger(__name__)


async def main():
    '''Запуск бота'''
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    logger.info("Старт бота")

    config: BotConfig = BotConfig.from_env()

    storage = RedisStorage(redis=r)

    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher(storage=storage)

    # Настраиваем меню (кнопки)
    await set_main_menu(bot)

    logger.info("Подключение роутеров")

    dp.include_router(router_common)
    dp.include_router(router_add_tasks)
    dp.include_router(router_delete_tasks)
    dp.include_router(router_done_tasks)
    dp.include_router(router_show_tasks)
    dp.include_router(router_auth)
    dp.include_router(router_correct_task)

    logger.info("Подклбчение middleware")

    router_add_tasks.message.middleware(Token_Middleware())
    router_add_tasks.callback_query.middleware(Token_Middleware())

    router_delete_tasks.message.middleware(Token_Middleware())
    router_delete_tasks.callback_query.middleware(Token_Middleware())

    router_done_tasks.message.middleware(Token_Middleware())
    router_done_tasks.callback_query.middleware(Token_Middleware())


    router_show_tasks.message.middleware(Token_Middleware())
    router_show_tasks.callback_query.middleware(Token_Middleware())

    router_correct_task.message.middleware(Token_Middleware())

    logger.info("Запуск бота")

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await dp.storage.close() # закрываем 
        await bot.session.close() # закрываем сессию
        await r.close() # закрываем соединение с Redis
        await api_client.close() # закрываем соединение с API

if __name__ == "__main__":
    asyncio.run(main())