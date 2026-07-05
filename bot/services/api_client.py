import httpx
from bot.config import BotConfig

from app.models.enum import Status, Priority, SortOrderId

config = BotConfig.from_env()
 
class TaskAPIClient:
    '''Клиент для работы с API'''
    def __init__(self):
        self._client = httpx.AsyncClient(
            base_url=config.API_URL,
            timeout=10 # бросит исключение в случае превышения таймаута
        )


    async def register(self, email: str, password: str):
        '''Регистрация'''
        response = await self._client.post(
            "/auth/register",
            json={
                "email": email,
                "password": password
            }
        )
        response.raise_for_status()
        return response.json()
    
    async def login(self, email: str, password: str):
        '''Авторизация'''
        response = await self._client.post(
            "/auth/login",
            json={
                "email": email,
                "password": password
            }
        )
        response.raise_for_status()
        return response.json()

    async def get_tasks(self, token: str, status: Status = None, priority: Priority = None, order_by: SortOrderId = None):
        '''Получить все задачи'''
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
            params=params,  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        response.raise_for_status()
        return response.json()  
        
    async def create_task(self, title: str, description: str, priority: Priority = None, token: str = None):
        '''Создать задачу'''
        params = {
            "title": title,
            "description": description
        }
        if priority is not None:
            params["priority"] = priority

        response = await self._client.post(
            "/tasks/",
            json=params,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        response.raise_for_status()
        return response.json()
        
    async def update_task(self, task_id: int, data: dict):
        '''Обновить задачу (полностью)'''
        response = await self._client.put(
            f"/tasks/{task_id}",
            json=data
        )
        response.raise_for_status()
        return response.json()
        
    async def patch_task(self, task_id: int, data: dict, token: str):
        '''Обновить задачу (частично)'''
        response = await self._client.patch(
            f"/tasks/{task_id}",
            json=data,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        response.raise_for_status()
        return response.json()
        
    async def delete_task(self, task_id: int, token: str):
        '''Удалить задачу'''
        response = await self._client.delete(
            f"/tasks/{task_id}",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response
    
    async def close(self):
        '''Закрытие клиента'''
        await self._client.aclose()


api_client = TaskAPIClient()