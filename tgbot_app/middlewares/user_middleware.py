from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from common.db_api import get_or_create_user


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        update: Update,
        data: Dict[str, Any],
    ) -> Any:
        command = data.get("command")
        args = command.args if command else None

        user = await get_or_create_user(
            tgid=update.event.from_user.id,
            username=update.event.from_user.username,
            first_name=update.event.from_user.first_name,
            last_name=update.event.from_user.last_name,
            link_id=args,
        )

        data["user"] = user

        return await handler(update, data)
