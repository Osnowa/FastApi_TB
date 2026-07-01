async def test_patch_task_priority(auth_client):
    '''Проверка обновления задачи (что меняется только priority)'''
    await auth_client.post(
        "/tasks/",
        json={
            "title": "test_title",
            "description": "test_description",
            "priority": "high"
        }
    )

    await auth_client.patch(
        "/tasks/1",
        json={
            "priority": "medium"
        }
    )

    result = await auth_client.get(
        "/tasks/1"
    )

    assert result.status_code == 200
    assert result.json()["priority"] == "medium"
    assert result.json()["description"] == "test_description"
    assert result.json()["title"] == "test_title"

async def test_patch_not_found_task(auth_client):
    '''Проверка обновления несуществующей задачи'''
    await auth_client.patch(
        "/tasks/1",
        json={
            "priority": "medium"
        }
    )

    result = await auth_client.get(
        "/tasks/1"
    )

    assert result.status_code == 404

async def test_patch_task_status(auth_client):
    '''Проверка обновления задачи (что меняется только status)'''
    # 1. Создаем реальную задачу через API
    response = await auth_client.post(
        "/tasks/",
        json={
            "title": "test_title",
            "description": "test_description"
        }
    )
    assert response.status_code == 201
    task_id = response.json()["id"]
    
    # 2. Проверяем, что задача создалась
    response = await auth_client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "new"
    
    # 3. Меняем статус через PATCH
    response = await auth_client.patch(
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
    response = await auth_client.get(f"/tasks/{task_id}")
    assert response.json()["status"] == "in_progress"
    
async def test_patch_garbage_status(auth_client):
    '''Проверка обновелния, с мусорным значением статуса'''
    response = await auth_client.patch(
        "/tasks/1",
        json={
            "status": "invalid"
        }
    )
    assert response.status_code == 422

async def test_patch_garbage_priority(auth_client):
    '''Проверка обновелния, с мусорным значением приоритета'''
    response = await auth_client.patch(
        "/tasks/1",
        json={
            "priority": "invalid"
        }
    )
    assert response.status_code == 422