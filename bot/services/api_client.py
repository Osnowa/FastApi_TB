import httpx
from bot.config import BotConfig

from app.models.enum import Status, Priority, SortOrderId

config = BotConfig.from_env()
 
class TaskAPIClient:
    def __init__(self):
        self._client = httpx.AsyncClient(
            base_url=config.API_URL,
            timeout=10 # бросит исключение в случае превышения таймаута
        )

    async def get_tasks(self, status: Status = None, priority: Priority = None, order_by: SortOrderId = None):
        params = {}
        if status is not None:
            params["status"] = status
        if priority is not None:
            params["priority"] = priority
        if order_by is not None:
            params["order_by"] = order_by
        
        # httpx сам соберет правильный URL
        response = await self._client.get(
            "/tasks/",
            params=params  # 👈 Передаем словарь параметров
        )
        response.raise_for_status()
        return response.json()  
        
    async def create_task(self, title: str, description: str, priority: Priority = None):
        params = {
            "title": title,
            "description": description
        }
        if priority is not None:
            params["priority"] = priority

        response = await self._client.post(
            "/tasks/",
            json=params
        )
        response.raise_for_status()
        return response.json()
        
    async def update_task(self, task_id: int, data: dict):
        response = await self._client.put(
            f"/tasks/{task_id}",
            json=data
        )
        response.raise_for_status()
        return response.json()
        
    async def patch_task(self, task_id: int, data: dict):
        response = await self._client.patch(
            f"/tasks/{task_id}",
            json=data
        )
        response.raise_for_status()
        return response.json()
        
    async def delete_task(self, task_id: int):
        response = await self._client.delete(
            f"/tasks/{task_id}"
        )

        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response
    
    async def close(self):
        '''Закрытие клиента'''
        await self._client.aclose()


api_client = TaskAPIClient()