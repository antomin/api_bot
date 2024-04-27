from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.enums import ChatMemberStatus
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, TelegramObject)

from common.models import User
from common.settings import settings


class ChannelMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        command = data.get("command")

        user: User = data["user"]

        if user.is_admin or user.tariff_id or (command and command.command == "start") or not settings.TARGET_CHAT:
            return await handler(event, data)

        status = await event.bot.get_chat_member(chat_id=settings.TARGET_CHAT, user_id=event.from_user.id)

        if status.status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR):
            return await handler(event, data)

        text = "Чтобы пользоваться самым лучшим ботом необходимо подписаться на наш канал!"
        markup = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Подписаться", url=f"https://t.me/{settings.TARGET_CHAT}")]]
        )

        if isinstance(event, CallbackQuery):
            await event.answer()
            event = event.message

        await event.answer(text=text, reply_markup=markup, disable_web_page_preview=True)
