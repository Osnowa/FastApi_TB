# Модель данных для базы данных в SQLite и SQLAlchemy


from sqlalchemy.orm import Mapped, mapped_column

from database import Base  # наш общий Base

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] # название задачи 
    description: Mapped[str] # описание задачи
    status: Mapped[str] = mapped_column(default="new") # статус задачи
    priority: Mapped[int | None] # приоритет