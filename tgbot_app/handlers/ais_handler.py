from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from common.settings import settings
from tgbot_app.keyboards import gen_ai_types_kb
from tgbot_app.utils.callbacks import ProfileCallback
from tgbot_app.utils.enums import DefaultCommands, MainButtons, ProfileButtons
from tgbot_app.utils.text_variables import AIS_TEXT

router = Router()


@router.message(Command(DefaultCommands.ais.name))
@router.message(F.text == MainButtons.AIS.value)
@router.callback_query(ProfileCallback.filter(F.action == ProfileButtons.AIS))
async def show_ai_types(message: Message | CallbackQuery, state: FSMContext):
    await state.clear()

    if isinstance(message, CallbackQuery):
        await message.answer()
        message = message.message

    await message.answer(text=AIS_TEXT.format(app_name=settings.APP_NAME), reply_markup=await gen_ai_types_kb())
