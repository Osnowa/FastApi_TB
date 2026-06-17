# схемы данных для FastAPI на получение и отправку
from pydantic import BaseModel, ConfigDict


class TaskBse(BaseModel):
    '''Базовая схема'''
    title: str
    description: str

class Task_add(TaskBse):
    '''Добавление задачи'''
    priority: int | None = None

class Task_puch(TaskBse):
    '''Отправка задачи пользователю'''
    id: int
    status: str
    priority: int | None 

    # для чтения схемы через pydantic и через точку
    model_config = ConfigDict(from_attributes=True)
