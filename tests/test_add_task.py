async def test_add_task(client):
    '''Проверка добавления задачи (базовый случай)'''
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


async def test_add_task_no_title(client):
    '''Проверка добавления задачи без title'''
    response = await client.post(
        "/tasks/",
        json={
            "description": "test_description"
        }
    )

    assert response.status_code == 422