async def test_put_task(client, db):
    '''Проверка частичного обновления задачи'''
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