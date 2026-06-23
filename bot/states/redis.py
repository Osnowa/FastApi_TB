import redis.asyncio as aioredis
from bot.config import BotConfig

config = BotConfig.from_env()

# настраиваем соединения, чтобы каждый раз не создавать новое
pool = aioredis.ConnectionPool.from_url(
    config.REDIS_URL,
    max_connections = 10,
    decode_responses = True
)

# Инициализация Redis
r = aioredis.Redis(connection_pool = pool)