from fastapi import FastAPI
import uvicorn
from routers.tasks import router as task_router

from contextlib import asynccontextmanager
from database import create_table, disponse_engine, SessionDep

from models.tasks import Task 

@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Создание таблиц и закрытие соединения с базой данных'''
    await create_table()
    yield
    # При остановке закрываем соединение с базой данных
    await disponse_engine()

# создаем приложение
app = FastAPI(lifespan=lifespan)
# подключаем роутеры
app.include_router(task_router)



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)