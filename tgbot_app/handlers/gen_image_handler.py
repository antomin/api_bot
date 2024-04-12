import uuid

from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, URLInputFile
from aiogram.utils.chat_action import ChatActionSender

from common.db_api import change_balance, create_image_query, update_object
from common.enums import ImageAction, ImageModels
from common.models import User
from common.settings import settings
from tgbot_app.keyboards import gen_img_model_kb, gen_midjourney_kb
from tgbot_app.services import neiro_api
from tgbot_app.services.neiro_api import GenerationStatus
from tgbot_app.utils.callbacks import AiTypeCallback, MJCallback
from tgbot_app.utils.enums import AiTypeButtons
from tgbot_app.utils.image_generations import run_mj_generation, run_image_generation
from tgbot_app.utils.misc import (can_send_query, gen_img_settings_text,
                                  handle_voice_prompt, send_no_balance_msg,
                                  translate_text)
from tgbot_app.utils.states import GenerationState
from tgbot_app.utils.text_variables import (BAN_TEXT, ERROR_MAIN_TEXT,
                                            MJ_CAPTION)

router = Router()


@router.callback_query(AiTypeCallback.filter(F.type == AiTypeButtons.IMAGE))
async def image_generation(callback: CallbackQuery, user: User, state: FSMContext):
    await callback.answer()

    text = gen_img_settings_text(user)
    markup = await gen_img_model_kb(user)

    await callback.message.answer(text=text, reply_markup=markup)

    await state.set_state(GenerationState.IMAGE)


@router.message(GenerationState.IMAGE)
async def image_generation(message: Message, user: User, state: FSMContext):
    model = user.img_model

    if not can_send_query(user=user, model=model):
        await send_no_balance_msg(user=user, bot=message.bot)
        return

    if message.voice:
        prompt = await handle_voice_prompt(message=message, user=user)
    elif message.photo:
        await message.answer(text=f"🚧 Данная функция в разработке. Следите за новостями.")
        return
    elif message.text:
        prompt = message.text
    else:
        return

    if model != ImageModels.KANDINSKY:
        status = await message.answer("🌐 Переводим Ваш запрос...")
        prompt = await translate_text(text=prompt, message=message)
    else:
        status = await message.answer("🚶‍♂️🚶‍♀️ Ваш запрос в очереди на генерацию..")

    await status.edit_text("🚶‍♂️🚶‍♀️ Ваш запрос в очереди на генерацию...")

    await state.set_state(GenerationState.IN_PROCESS)
    await change_balance(user=user, model=settings.MODELS[model])

    match model:
        case ImageModels.MIDJOURNEY:
            result = await run_mj_generation(action=ImageAction.IMAGINE, status=status, prompt=prompt)
        case ImageModels.DALLE_2 | ImageModels.DALLE_3:
            await status.edit_text("🖌️ Рисуем Ваше изображение...")
            img_query = await create_image_query(id=str(uuid.uuid4()), user_id=user.id, model=model,
                                                 status=GenerationStatus.IN_PROCESS)
            result = await neiro_api.dalle_imagine(model=model, prompt=prompt)
            await update_object(img_query, status=result.status, result=result.result)
        case _:
            result = await run_image_generation(model=model, prompt=prompt, status=status)

    await status.delete()

    if not result.success:
        await change_balance(user=user, model=settings.MODELS[model], add=True)
        text = BAN_TEXT if result.status == GenerationStatus.BANNED else ERROR_MAIN_TEXT
        await message.answer(text)
        await state.set_state(GenerationState.IMAGE)
        return

    async with ChatActionSender(bot=message.bot, chat_id=message.from_user.id, action=ChatAction.UPLOAD_PHOTO):
        photo = URLInputFile(result.result)

        if model == ImageModels.MIDJOURNEY:
            caption = MJ_CAPTION
            markup = await gen_midjourney_kb(result.task_id)
        else:
            caption = markup = None

        await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)
        await state.set_state(GenerationState.IMAGE)


@router.callback_query(MJCallback.filter())
async def run_midjourney_action(callback: CallbackQuery, callback_data: MJCallback, user: User, state: FSMContext):
    await callback.answer()

    if not can_send_query(user=user, model=ImageModels.MIDJOURNEY):
        await send_no_balance_msg(user=user, bot=callback.bot)
        return

    action = callback_data.action
    index = callback_data.index
    task_id = callback_data.task_id

    status = await callback.message.answer("🚶‍♂️🚶‍♀️ Ваш запрос в очереди на генерацию...")
    await change_balance(user=user, model=settings.MODELS[ImageModels.MIDJOURNEY])
    await state.set_state(GenerationState.IN_PROCESS)

    result = await run_mj_generation(action=action, status=status, task_id=task_id, index=index)

    await status.delete()

    if not result.success:
        await change_balance(user=user, model=settings.MODELS[ImageModels.MIDJOURNEY], add=True)
        text = BAN_TEXT if result.status == GenerationStatus.BANNED else ERROR_MAIN_TEXT
        await callback.message.answer(text)
        await state.set_state(GenerationState.IMAGE)
        return

    async with ChatActionSender(bot=callback.bot, chat_id=callback.from_user.id, action=ChatAction.UPLOAD_PHOTO):
        photo = URLInputFile(result.result, filename=result.result.split("/")[-1])

        if action == ImageAction.VARIATION:
            caption = MJ_CAPTION
            markup = await gen_midjourney_kb(result.task_id)
            await callback.message.answer_photo(photo=photo, caption=caption, reply_markup=markup)
        else:
            await callback.message.answer_photo(photo=photo)
            await callback.message.answer_document(document=photo, disable_notification=True)

        await state.set_state(GenerationState.IMAGE)
