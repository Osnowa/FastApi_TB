from dataclasses import dataclass
from environs import Env

@dataclass
class Config:
    DATABASE_URL: str 

    @classmethod
    def from_env(cls):
        env = Env()
        env.read_env()
        return cls(DATABASE_URL=env.str("DATABASE_URL"))