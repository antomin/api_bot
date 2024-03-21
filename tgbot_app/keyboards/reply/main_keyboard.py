from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from tgbot_app.utils.enums import MainButtons


async def main_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for btn in MainButtons:
        builder.button(text=btn)
    builder.adjust(2, 2, 1)

    return builder.as_markup(resize_keyboard=True)
