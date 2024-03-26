from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from common.models import User
from tgbot_app.keyboards import (gen_ai_types_kb, gen_img_model_kb,
                                 gen_txt_settings_kb)
from tgbot_app.utils.callbacks import AiTypeCallback, ProfileCallback
from tgbot_app.utils.enums import (AiTypeButtons, DefaultCommands, MainButtons,
                                   ProfileButtons)
from tgbot_app.utils.misc import gen_img_settings_text, gen_txt_settings_text
from tgbot_app.utils.states import GenerationState

router = Router()


@router.message(Command(DefaultCommands.ais.name))
@router.message(F.text == MainButtons.AIS.value)
@router.callback_query(ProfileCallback.filter(F.action == ProfileButtons.AIS))
async def show_ai_types(message: Message | CallbackQuery, state: FSMContext):
    await state.clear()

    if isinstance(message, CallbackQuery):
        await message.answer()
        message = message.message

    markup = await gen_ai_types_kb()
    text = ("🔹 Агрегатор <a href='https://Нейросети.com'>Нейросети.com</a> поможет с решением Ваших повседневных "
            "задач с помощью нейросетей и автоматизирует процессы Вашей работы.\n\n"
            "💎 - Используйте ваши токены чтобы пользоваться нейросетями. Стоимость использование некоторых "
            "нейросетей может показаться дорогим, это связано с их реальной стоимость у разработчиков.")

    await message.answer(text=text, reply_markup=markup, disable_web_page_preview=True)


@router.callback_query(AiTypeCallback.filter(F.type == AiTypeButtons.TEXT))
async def text_generation(callback: CallbackQuery, user: User, state: FSMContext):
    await state.set_state(GenerationState.TEXT)
    await callback.answer()

    text = gen_txt_settings_text(user)
    markup = await gen_txt_settings_kb(user)

    await callback.message.answer(text=text, reply_markup=markup)


@router.callback_query(AiTypeCallback.filter(F.type == AiTypeButtons.IMAGE))
async def image_generation(callback: CallbackQuery, user: User, state: FSMContext):
    await state.set_state(GenerationState.IMAGE)
    await callback.answer()

    text = gen_img_settings_text(user)
    markup = await gen_img_model_kb(user)

    await callback.message.answer(text=text, reply_markup=markup)
