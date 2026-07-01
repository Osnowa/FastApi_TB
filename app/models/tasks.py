# Модель данных для базы данных в SQLite и SQLAlchemy
from sqlalchemy import Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy.sql import func

from app.database import Base  # наш общий Base

from app.models.enum import Status, Priority

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] # название задачи 
    description: Mapped[str] # описание задачи
    status: Mapped[Status | None] = mapped_column(SQLEnum(Status), default=Status.new) # статус задачи
    priority: Mapped[Priority | None] = mapped_column(SQLEnum(Priority), default=None) # приоритет
    created_at: Mapped[datetime] = mapped_column(server_default=func.now()) # дата создания

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))