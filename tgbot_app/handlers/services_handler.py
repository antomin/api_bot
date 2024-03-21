from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tgbot_app.keyboards import main_kb
from tgbot_app.utils.enums import DefaultCommands, MainButtons

router = Router()


@router.message(Command(DefaultCommands.services.name))
@router.message(F.text == MainButtons.SERVICES.value)
async def services(message: Message, state: FSMContext):
    await state.clear()

    text = "SERVICES"
    markup = await main_kb()

    await message.answer(text=text, reply_markup=markup)
