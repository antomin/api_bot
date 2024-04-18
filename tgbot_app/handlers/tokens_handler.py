from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from common.models import User
from tgbot_app.keyboards import gen_tokens_kb
from tgbot_app.utils.callbacks import ProfileCallback
from tgbot_app.utils.enums import DefaultCommands, ProfileButtons
from tgbot_app.utils.text_generators import gen_token_text

router = Router()


@router.callback_query(ProfileCallback.filter(F.action == ProfileButtons.TOKENS))
@router.message(Command(DefaultCommands.tokens.name))
async def tokens(message: Message | CallbackQuery, user: User):
    if isinstance(message, CallbackQuery):
        await message.answer()
        message = message.message

    text = gen_token_text(user)
    markup = await gen_tokens_kb(user)

    await message.answer(text=text, reply_markup=markup, disable_web_page_preview=True)
