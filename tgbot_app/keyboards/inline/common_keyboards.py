from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot_app.utils.callbacks import ProfileCallback
from tgbot_app.utils.enums import ProfileButtons


async def gen_error_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🤖 Нейросети", callback_data=ProfileCallback(action=ProfileButtons.AIS))
    builder.button(text="📲 Сервисы", callback_data="_")  # TODO
    builder.button(text="❓Помощь", callback_data="_")  # TODO

    return builder.adjust(1).as_markup()
