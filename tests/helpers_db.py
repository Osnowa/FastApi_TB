import pytest_asyncio
from httpx import AsyncClient

@pytest_asyncio.fixture(scope='function')
async def create_tasks(client: AsyncClient):
    for i in range(1,4):
        await client.post(
            "/tasks/",
            json={
                "title": f"test_title{i}",
                "description": f"test_description{i}"
            }
        )