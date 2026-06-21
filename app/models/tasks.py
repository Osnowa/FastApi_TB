# Модель данных для базы данных в SQLite и SQLAlchemy
from enum import Enum
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base  # наш общий Base

from app.models.enum import Status, Priority

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] # название задачи 
    description: Mapped[str] # описание задачи
    status: Mapped[Status | None] = mapped_column(SQLEnum(Status), default=Status.new) # статус задачи
    priority: Mapped[Priority | None] = mapped_column(SQLEnum(Priority), default=None) # приоритет