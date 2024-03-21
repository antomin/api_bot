from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from common.models import User
from tgbot_app.keyboards import gen_profile_kb
from tgbot_app.utils.enums import DefaultCommands, MainButtons
from tgbot_app.utils.misc import gen_profile_text

router = Router()


@router.message(Command(DefaultCommands.profile.name))
@router.message(F.text == MainButtons.PROFILE.value)
async def profile(message: Message, user: User, state: FSMContext):
    await state.clear()

    text = await gen_profile_text(user)
    markup = await gen_profile_kb()

    await message.answer(text=text, reply_markup=markup)
