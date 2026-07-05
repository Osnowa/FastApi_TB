from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from bot.states.redis import r

PUBLIC_COMMANDS = {
    "start",
    "help",
    "login",
    "register",
}

class Token_Middleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:

        user_id = event.from_user.id
        token = await r.hget(f"token:{user_id}", "token")
        
        if token:
            data['token'] = token
        else:
            # Отправляем сообщение пользователю
            if isinstance(event, Message):
                await event.answer("🔒 Вы не авторизованы! Используйте /login")
            elif isinstance(event, CallbackQuery):
                await event.answer("🔒 Авторизуйтесь!", show_alert=True)
            return  # Прерываем обработку

        result = await handler(event, data)
        return result