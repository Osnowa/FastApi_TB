import logging

import asyncio
from aiogram import Bot, Dispatcher
from bot.config import BotConfig
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from bot.handlers.starts import router as router_start
from bot.handlers.tasks import router as router_tasks

from bot.services.api_client import TaskAPIClient

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

    logger.info("Подключение роутеров")
    dp.include_router(router_start)
    dp.include_router(router_tasks)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()
        await r.close()
        await api_client.close()

if __name__ == "__main__":
    asyncio.run(main())