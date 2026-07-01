from dataclasses import dataclass
from environs import Env

@dataclass
class Config:
    DATABASE_URL: str 
    ALEMBIC_DATABASE_URL: str
    SECRET_KEY: str

    @classmethod
    def from_env(cls):
        env = Env()
        env.read_env()
        return cls(
            DATABASE_URL = env.str("DATABASE_URL"),
            ALEMBIC_DATABASE_URL = env.str("ALEMBIC_DATABASE_URL"),
            SECRET_KEY = env.str("SECRET_KEY")
        )