from app.repository import Repository
from app.schemas.tasks import TaskCreate


async def test_add_task(client):
    response = await client.post(
        "/tasks/",
        json={
            "title": "test_title",
            "description": "test_description"
        }
    )

    assert response.status_code == 201
    assert response.json()["title"] == "test_title"
    assert response.json()["description"] == "test_description"

async def test_get_tasks(client, db):
    # добавим задачу
    await client.post(
        "/tasks/",
        json={
            "title": "test_title",
            "description": "test_description"
        }
    )
    # получим задачи
    response = await client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "test_title"
    assert response.json()[0]["description"] == "test_description"

    # добавим ещё задачу
    await client.post(
        "/tasks/",
        json={
            "title": "test_title2",
            "description": "test_description2"
        }
    )
    # получим уже обе задачи
    response = await client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[1]["title"] == "test_title2"
    assert response.json()[1]["description"] == "test_description2"

async def test_get_task_id(client, db):
    # Вначале проверка получения несуществующей задачи
    response = await client.get("/tasks/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Задача не найдена"

    repo = Repository(db)
    # добавим задачу
    await repo.add_task(TaskCreate(title="test_title_id", description="test_description"))
    # получим задачу по id
    response = await client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json()["title"] == "test_title_id"
    assert response.json()["description"] == "test_description"

async def test_put_task(client, db):
    # добавим задачу
    await client.post(
        "/tasks/",
        json={
            "title": "test_title",
            "description": "test_description"
        }
    )
    task = await client.get("/tasks/1")
    assert task.status_code == 200
    assert task.json()["title"] == "test_title"
    assert task.json()["description"] == "test_description"

    # изменяем задачу
    await client.put(
        "/tasks/1",
        json={
            "title": "test_title_changed",
            "description": "test_description_changed"
        }
    )
    task1 = await client.get("/tasks/1")
    assert task1.status_code == 200
    assert task1.json()["title"] == "test_title_changed"
    assert task1.json()["description"] == "test_description_changed"


async def test_delete_task(client):
    response = await client.delete("/tasks/1")
    assert response.status_code == 404

    await client.post(
        "/tasks/",
        json={
            "title": "test_title",
            "description": "test_description"
        }
    )
    
    response = await client.delete("/tasks/1")
    assert response.status_code == 204