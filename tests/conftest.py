import pytest_asyncio
from app.database import Base, get_session
from app.auth.dependencies import get_current_user
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.models.users import User



# тестовая база
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    TEST_DATABASE_URL
    )

TestAsyncSession = async_sessionmaker(engine, expire_on_commit=False)

@pytest_asyncio.fixture(scope = 'session', autouse = True)# применяем к всем тестам автоматически, на весь запуск
async def setur_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) # создаем все таблицы

    yield
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) # удаляем после тестов все таблицы

@pytest_asyncio.fixture
async def db():
    connection = await engine.connect() # открываем соединение
    await connection.begin()
    
    # создаем сессию поверх этого соединения
    session = AsyncSession(bind = connection, expire_on_commit = False)

    yield session # тест работает с этой сессией

    await session.close()
    await connection.rollback() # тест не оставляет следов, откат 
    await connection.close()

@pytest_asyncio.fixture
async def client(db):
    '''Тестовый клиент (наш веб-сервер), который использует тестовую базу данных'''
    # заменяем зависимость get_db
    async def override_get_session():
        yield db

    # Создаем тестовый клиент
    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides = {}


@pytest_asyncio.fixture
async def auth_client(db):
    '''Подменяем авторизированного пользователя'''
    fake_user = User(
        email="test@pochta.ru",
        hashed_password="fake_hashed_password"
    )
    db.add(fake_user)
    await db.commit()
    await db.refresh(fake_user)  # получаем настоящий id из БД

    async def override_get_session():
        yield db

    async def override_get_current_user():
        return fake_user  # теперь fake_user.id реально существует в БД

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_current_user] = override_get_current_user

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides = {}

@pytest_asyncio.fixture(scope='function')
async def create_tasks(auth_client):
    for i in range(1,4):
        await auth_client.post(
            "/tasks/",
            json={
                "title": f"test_title{i}",
                "description": f"test_description{i}"
            }
        )
