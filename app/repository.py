# Файл для работы с базой данных
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.tasks import Task_add
from app.models.tasks import Task


class Repository:
    '''Репозитории для работы с базой данных'''
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_task(self, data: Task_add):
        '''Добавление задачи в базу данных'''
        task = Task(**data.model_dump()) # ORM умеет работать только с своими моделями
        self.session.add(task) # добавление задачи в базу данных
        await self.session.commit()
        await self.session.refresh(task)
        # возвращаем задачу для post, по схеме pydantic
        return task 
    
    async def get_all_tasks(self):
        '''Получение всех задач из базы данных'''
        result = await self.session.execute(select(Task))
        return result.scalars().all()
    
    async def get_task_by_id(self, task_id: int):
        '''Получение задачи по id'''
        result = await self.session.execute(select(Task).where(Task.id == task_id))
        return result.scalars().one_or_none()
    
    async def update_task(self, task_id: int, data: Task_add):
        '''Обновление задачи в базе данных'''
        task = await self.get_task_by_id(task_id)
        if not task:
            return None
        stmt = update(Task).where(Task.id == task_id).values(**data.model_dump())
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_task_by_id(task_id)
    
    async def delete_task(self, task_id: int):
        '''Удаление задачи из базы данных'''
        task = await self.get_task_by_id(task_id)
        if not task:
            return None
        else:
            await self.session.delete(task)
            await self.session.commit()