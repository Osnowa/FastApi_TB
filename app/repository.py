# Файл для работы с базой данных
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.tasks import TaskCreate, TaskPatch, TaskUpdate
from app.models.tasks import Task
from app.models.users import User
from app.models.enum import Status, Priority, SortOrderId


class Repository:
    '''Репозитории для работы с базой данных'''
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_task(self, data: TaskCreate, user_id: int):
        '''Добавление задачи в базу данных'''
        task = Task(**data.model_dump(), user_id=user_id) # ORM умеет работать только с своими моделями
        self.session.add(task) # добавление задачи в базу данных
        await self.session.commit()
        await self.session.refresh(task)
        # возвращаем задачу для post, по схеме pydantic
        return task 
    
    async def get_all_tasks(
            self, 
            user_id: int,
            status: Status | None = None, 
            priority: Priority | None = None, 
            order_by: SortOrderId | None = None,
            title: str | None = None,
            limit: int | None = 10,
            offset: int | None = 0
            ):
        '''Получение всех задач из базы данных'''


        stmt = select(Task).where(Task.user_id == user_id)

        if title is not None:
            stmt = stmt.where(Task.title.contains(title))

        if status is not None:
            stmt = stmt.where(Task.status == status)

        if priority is not None:
            stmt = stmt.where(Task.priority == priority)

        if order_by is not None:
            if order_by == SortOrderId.id_asc:
                stmt = stmt.order_by(Task.id.asc())
            elif order_by == SortOrderId.id_desc:
                stmt = stmt.order_by(Task.id.desc())

        stmt = stmt.limit(limit).offset(offset)

        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_task_by_id(self, task_id: int, user_id: int):
        '''Получение задачи по id'''
        result = await self.session.execute(select(Task).where(Task.id == task_id and Task.user_id == user_id))
        return result.scalars().one_or_none()
    
    async def update_task(self, task_id: int, data: TaskUpdate, user_id: int):
        '''Обновление задачи в базе данных (полная замена)'''
        task = await self.get_task_by_id(task_id, user_id)
        if not task:
            return None
        stmt = update(Task).where(Task.id == task_id and Task.user_id == user_id).values(**data.model_dump(), user_id=user_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_task_by_id(task_id, user_id)
    
    async def patch_task(self, task_id: int, data: TaskPatch, user_id: int):
        '''Частичное обновление задачи в базе данных'''
        task = await self.get_task_by_id(task_id, user_id)
        if not task:
            return None
        stmt = update(Task).where(Task.id == task_id and Task.user_id == user_id).values(**data.model_dump(exclude_unset=True))
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_task_by_id(task_id, user_id)
    
    async def delete_task(self, task_id: int, user_id: int):
        '''Удаление задачи из базы данных'''
        task = await self.get_task_by_id(task_id, user_id)
        if not task:
            return None
        else:
            await self.session.delete(task)
            await self.session.commit()

    # --- Логика для User ---

    async def get_user(self, email):
        '''Получение пользователя по email'''
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().one_or_none()
    
    async def add_user(self, data_user):
        '''Добавление пользователя в базу данных'''
        user = User(
            email=data_user.email,
            hashed_password=data_user.password  # 👈 Здесь уже хеш
        )
        self.session.add(user) # запомни этот обьект
        await self.session.commit() # отправлено в бд
        await self.session.refresh(user) # обновление
        return user