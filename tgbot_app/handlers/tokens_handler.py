from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tgbot_app.keyboards import main_kb
from tgbot_app.utils.enums import DefaultCommands

router = Router()


@router.message(Command(DefaultCommands.tokens.name))
async def tokens_start(message: Message, state: FSMContext):
    await state.clear()

    text = "TOKENS"
    markup = await main_kb()

    await message.answer(text=text, reply_markup=markup)
