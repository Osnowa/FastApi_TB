from fastapi import FastAPI
import uvicorn
from app.routers.tasks import router as task_router

from contextlib import asynccontextmanager
from app.database import disponse_engine


# Метод, который работает про включении и выкл приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("app start")
    yield
    print("app stop")
    await disponse_engine()

app = FastAPI(lifespan=lifespan)

# подключаем роутеры
app.include_router(task_router)



if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)