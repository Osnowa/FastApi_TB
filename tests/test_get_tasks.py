from app.repository import Repository
from app.schemas.tasks import TaskCreate


async def test_get_tasks(auth_client):
    '''Проверка получения задач (базовый случай)'''
    # добавим задачу
    await auth_client.post(
        "/tasks/",
        json={
            "title": "test_title",
            "description": "test_description"
        }
    )
    # получим задачи
    response = await auth_client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "test_title"
    assert response.json()[0]["description"] == "test_description"

    # добавим ещё задачу
    await auth_client.post(
        "/tasks/",
        json={
            "title": "test_title2",
            "description": "test_description2"
        }
    )
    # получим уже обе задачи
    response = await auth_client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[1]["title"] == "test_title2"
    assert response.json()[1]["description"] == "test_description2"

async def test_get_task_id(auth_client, db):
    '''Проверка получения задачи по id'''
    # Вначале проверка получения несуществующей задачи
    response = await auth_client.get("/tasks/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Задача не найдена"

    # добавим задачу
    await auth_client.post(
        "/tasks/",
        json={
            "title": "test_title_id",
            "description": "test_description"
        }
    )
    # получим задачу по id
    response = await auth_client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json()["title"] == "test_title_id"
    assert response.json()["description"] == "test_description"
    