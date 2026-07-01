async def test_put_task(auth_client):
    '''Проверка частичного обновления задачи'''
    # добавим задачу
    await auth_client.post(
        "/tasks/",
        json={
            "title": "test_title",
            "description": "test_description"
        }
    )
    task = await auth_client.get("/tasks/1")
    assert task.status_code == 200
    assert task.json()["title"] == "test_title"
    assert task.json()["description"] == "test_description"

    # изменяем задачу
    await auth_client.put(
        "/tasks/1",
        json={
            "title": "test_title_changed",
            "description": "test_description_changed"
        }
    )
    task1 = await auth_client.get("/tasks/1")
    assert task1.status_code == 200
    assert task1.json()["title"] == "test_title_changed"
    assert task1.json()["description"] == "test_description_changed"


async def test_delete_task(auth_client):
    '''Проверка удаления задачи'''
    response = await auth_client.delete("/tasks/1")
    assert response.status_code == 404

    await auth_client.post(
        "/tasks/",
        json={
            "title": "test_title",
            "description": "test_description"
        }
    )
    
    response = await auth_client.delete("/tasks/1")
    assert response.status_code == 204