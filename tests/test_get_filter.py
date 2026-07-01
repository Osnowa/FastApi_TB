async def test_get_filter(auth_client, create_tasks):
    '''Тест по фильтру статус = new'''
    # меняем статус у 1 задачи
    await auth_client.patch(
        "/tasks/1",
        json={
            "status": "in_progress"
        }
    )

    response = await auth_client.get("/tasks/?status=new")
    assert response.status_code == 200
    assert len(response.json()) == 2

    response2 = await auth_client.get("/tasks/?status=in_progress")
    assert response2.status_code == 200
    assert len(response2.json()) == 1


async def test_get_filter_priority(auth_client, create_tasks):
    '''Тест по фильтру приоритет = high'''
    await auth_client.patch(
        "/tasks/1",
        json={
            "priority": "high"
        }
    )

    response = await auth_client.get("/tasks/?priority=high")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response2 = await auth_client.get("/tasks/?priority=medium")
    assert response2.status_code == 200
    assert len(response2.json()) == 0


async def test_get_filter_status_and_priority(auth_client, create_tasks):
    '''Тест по фильтру приоритет = high и статус = done'''
    await auth_client.patch(
        "/tasks/1",
        json={
            "priority": "high"
        }
    )

    await auth_client.patch(
        "/tasks/1",
        json={
            "status": "done"
        }
    )

    response = await auth_client.get("/tasks/?status=done&priority=high")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response2 = await auth_client.get("/tasks/?status=done&priority=medium")
    assert response2.status_code == 200
    assert len(response2.json()) == 0

async def test_get_tasks_no_valid_status(auth_client, create_tasks):
    '''Тест, где статус будет невалидным'''
    # Проверка на валидный статус
    response = await auth_client.get("/tasks/?status=new")
    assert response.status_code == 200

    # Проверка на невалидный статус
    response = await auth_client.get("/tasks/?status=invalid")
    assert response.status_code == 422

async def test_get_tasks_no_valid_priority(auth_client, create_tasks):
    '''Тест, где приоритет будет невалидным'''
    # Проверка на валидный приоритет
    response = await auth_client.get("/tasks/?priority=high")
    assert response.status_code == 200

    # Проверка на невалидный приоритет
    response = await auth_client.get("/tasks/?priority=invalid")
    assert response.status_code == 422