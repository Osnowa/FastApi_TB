from helpers_db import create_tasks
async def test_get_filter(client, create_tasks):
    '''Тест по фильтру статус = new'''
    # меняем статус у 1 задачи
    await client.patch(
        "/tasks/1",
        json={
            "status": "in_progress"
        }
    )

    response = await client.get("/tasks/?status=new")
    assert response.status_code == 200
    assert len(response.json()) == 2

    response2 = await client.get("/tasks/?status=in_progress")
    assert response2.status_code == 200
    assert len(response2.json()) == 1


async def test_get_filter_priority(client, create_tasks):
    '''Тест по фильтру приоритет = high'''
    await client.patch(
        "/tasks/1",
        json={
            "priority": "high"
        }
    )

    response = await client.get("/tasks/?priority=high")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response2 = await client.get("/tasks/?priority=medium")
    assert response2.status_code == 200
    assert len(response2.json()) == 0


async def test_get_filter_status_and_priority(client, create_tasks):
    '''Тест по фильтру приоритет = high и статус = done'''
    await client.patch(
        "/tasks/1",
        json={
            "priority": "high"
        }
    )

    await client.patch(
        "/tasks/1",
        json={
            "status": "done"
        }
    )

    response = await client.get("/tasks/?status=done&priority=high")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response2 = await client.get("/tasks/?status=done&priority=medium")
    assert response2.status_code == 200
    assert len(response2.json()) == 0