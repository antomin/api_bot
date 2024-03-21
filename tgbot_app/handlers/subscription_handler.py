from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tgbot_app.keyboards import main_kb
from tgbot_app.utils.enums import DefaultCommands, MainButtons

router = Router()


@router.message(Command(DefaultCommands.subscription.name))
@router.message(F.text == MainButtons.SUBSCRIPTION.value)
async def subscription(message: Message, state: FSMContext):
    await state.clear()

    text = "SUBSCRIPTION"
    markup = await main_kb()

    await message.answer(text=text, reply_markup=markup)
