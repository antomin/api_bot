import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommandScopeAllGroupChats, BotCommand, BotCommandScopeAllPrivateChats
from loguru import logger

from common.settings import settings
from tgbot_app.handlers import main_router
from tgbot_app.utils.enums import DefaultCommands
from tgbot_app.middlewares import UserMiddleware


def _set_loggers() -> None:
    logger.add("logs/bot.log", rotation="00:00", format="{time} {level} {message}", level="ERROR", enqueue=True)
    if settings.DEBUG:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)


def _connect_middlewares(dp: Dispatcher) -> None:
    dp.update.middleware.register(UserMiddleware())


async def _set_default_commands(bot: Bot) -> None:
    await bot.delete_my_commands()

    await bot.set_my_commands(commands=[], scope=BotCommandScopeAllGroupChats())
    await bot.set_my_commands(
        commands=[BotCommand(command=cmd.name, description=cmd.value) for cmd in DefaultCommands],
        scope=BotCommandScopeAllPrivateChats()
    )


async def main() -> None:
    _set_loggers()

    bot = Bot(token=settings.TG_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    await _set_default_commands(bot)
    dp.include_router(main_router)
    _connect_middlewares(dp)

    logger.info("Start polling...")

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
