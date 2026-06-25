# схемы данных для FastAPI на получение и отправку
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.models.enum import Status, Priority

class TaskBase(BaseModel):
    '''Базовая схема'''
    title: str
    description: str

    # для чтения схемы через pydantic и через точку
    model_config = ConfigDict(from_attributes=True)

class TaskCreate(TaskBase):
    '''Добавление задачи'''
    priority: Priority | None = None

class TaskUpdate(TaskBase):
    '''Изменение задачи (полное изменение)'''
    status: Status | None = None
    priority: Priority | None = None 

class TaskPatch(BaseModel):
    '''Изменение задачи (частичное изменение)'''
    title: str | None = None
    description: str | None = None
    status: Status | None = None
    priority: Priority | None = None

class TaskResponse(TaskBase):
    '''Ответ пользователю'''
    id: int
    status: Status | None
    priority: Priority | None
    created_at: datetime
