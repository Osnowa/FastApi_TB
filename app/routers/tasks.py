from fastapi import APIRouter

from shemas.tasks import Task_add
from database import SessionDep

router = APIRouter(
    prefix="/tasks", # роутер сам прикрепит префикс к эндпоинтам
    tags=["tasks"]
)

@router.post("/")
async def add_task(task: Task_add, session: SessionDep):
    pass