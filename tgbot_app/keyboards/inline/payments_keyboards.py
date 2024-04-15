from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from common.models import User
from tgbot_app.utils.callbacks import ProfileCallback
from tgbot_app.utils.enums import ProfileButtons


async def gen_no_tokens_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="💎 Купить токенов", callback_data=ProfileCallback(action=ProfileButtons.TOKENS))
    builder.button(text="💳 Оформить подписку", callback_data=ProfileCallback(action=ProfileButtons.PREMIUM))

    return builder.adjust(1).as_markup()
