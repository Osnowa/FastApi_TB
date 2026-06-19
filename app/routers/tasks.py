from fastapi import APIRouter, status, HTTPException

from app.schemas.tasks import Task_add, Task_puch
from ..database import SessionDep

from app.repository import Repository

router = APIRouter(
    prefix="/tasks", # роутер сам прикрепит префикс к эндпоинтам
    tags=["tasks"]
)

@router.post("/", response_model = Task_puch, status_code=status.HTTP_201_CREATED)
async def add_task(task: Task_add, session: SessionDep):
    '''Добавить задачу'''
    repo = Repository(session)
    return await repo.add_task(task)

@router.get("/", response_model=list[Task_puch], status_code=status.HTTP_200_OK)
async def get_tasks(session: SessionDep):
    '''Получить все задачи'''
    repo = Repository(session)
    return await repo.get_all_tasks()

@router.get('/{id}', response_model=Task_puch, status_code=status.HTTP_200_OK)
async def get_task_id(id: int , session: SessionDep):
    '''Получить задачу по id'''
    repo = Repository(session)
    result =  await repo.get_task_by_id(id)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
            )
    
@router.put('/{id}', response_model=Task_puch, status_code=status.HTTP_200_OK)
async def put_task(id: int, task: Task_add, session: SessionDep):
    '''Изменить задачу (полная замена)'''
    repo = Repository(session)
    result = await repo.get_task_by_id(id)
    if result:
        return await repo.update_task(id, task)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
            )
    
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int, session: SessionDep):
    '''Удалить задачу'''
    repo = Repository(session)
    result = await repo.get_task_by_id(id)
    if result:
        await repo.delete_task(id)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
            )