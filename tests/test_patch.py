
async def test_patch_task_priority(client, db):
    '''Проверка обновления задачи (что меняется только priority)'''
    await client.post(
        "/tasks/",
        json={
            "title": "test_title",
            "description": "test_description",
            "priority": "high"
        }
    )

    await client.patch(
        "/tasks/1",
        json={
            "priority": "medium"
        }
    )

    result = await client.get(
        "/tasks/1"
    )

    assert result.status_code == 200
    assert result.json()["priority"] == "medium"
    assert result.json()["description"] == "test_description"
    assert result.json()["title"] == "test_title"

async def test_patch_not_found_task(client, db):
    '''Проверка обновления несуществующей задачи'''
    await client.patch(
        "/tasks/1",
        json={
            "priority": "medium"
        }
    )

    result = await client.get(
        "/tasks/1"
    )

    assert result.status_code == 404

async def test_patch_task_status(client, db, mocker):
    '''Проверка обновления задачи (что меняется только status)'''
    # 1. Создаем реальную задачу через API
    response = await client.post(
        "/tasks/",
        json={
            "title": "test_title",
            "description": "test_description"
        }
    )
    assert response.status_code == 201
    task_id = response.json()["id"]
    
    # 2. Проверяем, что задача создалась
    response = await client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "new"
    
    # 3. Меняем статус через PATCH
    response = await client.patch(
        f"/tasks/{task_id}",
        json={"status": "in_progress"}
    )
    assert response.status_code == 200
    
    # 4. Проверяем, что статус изменился
    data = response.json()
    assert data["status"] == "in_progress"
    assert data["title"] == "test_title"
    assert data["description"] == "test_description"
    
    # 5. Проверяем через GET
    response = await client.get(f"/tasks/{task_id}")
    assert response.json()["status"] == "in_progress"
    