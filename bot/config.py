from environs import Env
from dataclasses import dataclass

@dataclass
class BotConfig:
    BOT_TOKEN: str
    API_URL: str
    REDIS_URL: str

    @classmethod
    def from_env(cls):
        env = Env()
        env.read_env()
        return cls(
            BOT_TOKEN = env.str("BOT_TOKEN"),
            API_URL = env.str("API_URL"),
            REDIS_URL = env.str("REDIS_URL")
        )   