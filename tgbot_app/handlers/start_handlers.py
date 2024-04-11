from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from common.settings import settings
from tgbot_app.keyboards import main_kb
from tgbot_app.utils.text_variables import START_TEXT

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=START_TEXT.format(app_name=settings.APP_NAME), reply_markup=await main_kb())
