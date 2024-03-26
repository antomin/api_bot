from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, FSInputFile

from common.db_api import update_object
from common.models import User
from common.settings import settings
from tgbot_app.keyboards import (gen_text_models_kb, gen_text_roles_kb,
                                 gen_txt_settings_kb, gen_main_speaker_kb, gen_speaker_category_kb, gen_img_model_kb)
from tgbot_app.utils.callbacks import (RoleCallback, TextModelCallback,
                                       TextSettingsCallback, SileroCallback, ImageModelCallback)
from tgbot_app.utils.enums import TextSettingsButtons, SileroAction
from tgbot_app.utils.misc import gen_txt_settings_text, gen_img_settings_text

router = Router()


@router.callback_query(TextSettingsCallback.filter(F.action == TextSettingsButtons.CONTEXT))
async def text_settings_context(callback: CallbackQuery, user: User):
    await update_object(user, context=(not user.context), update_relations=True)

    markup = await gen_txt_settings_kb(user)

    await callback.message.edit_reply_markup(reply_markup=markup)
    await callback.answer()


@router.callback_query(TextSettingsCallback.filter(F.action == TextSettingsButtons.MODEL))
async def text_settings_model(callback: CallbackQuery, user: User):
    markup = await gen_text_models_kb(user)

    await callback.message.edit_reply_markup(reply_markup=markup)
    await callback.answer()


@router.callback_query(TextModelCallback.filter())
async def set_text_model(callback: CallbackQuery, callback_data: TextModelCallback, user: User):
    if user.txt_model != callback_data.model:
        await update_object(user, txt_model=callback_data.model)

    text = gen_txt_settings_text(user)
    markup = await gen_txt_settings_kb(user)

    await callback.message.edit_text(text=text, reply_markup=markup)
    await callback.answer()


@router.callback_query(TextSettingsCallback.filter(F.action == TextSettingsButtons.ROLE))
async def text_settings_role(callback: CallbackQuery, user: User):
    markup = await gen_text_roles_kb(user)

    await callback.message.edit_reply_markup(reply_markup=markup)
    await callback.answer()


@router.callback_query(RoleCallback.filter())
async def set_text_role(callback: CallbackQuery, callback_data: RoleCallback, user: User):
    role_id = None if callback_data.role_id == 0 else callback_data.role_id

    if user.txt_model_role_id != callback_data.role_id:
        await update_object(user, txt_model_role_id=role_id, update_relations=True)

    markup = await gen_txt_settings_kb(user)

    await callback.message.edit_reply_markup(reply_markup=markup)
    await callback.answer()


@router.callback_query(TextSettingsCallback.filter(F.action == TextSettingsButtons.BACK))
async def text_settings_role_back(callback: CallbackQuery, user: User):
    markup = await gen_txt_settings_kb(user)

    await callback.message.edit_reply_markup(reply_markup=markup)
    await callback.answer()


@router.callback_query(TextSettingsCallback.filter(F.action == TextSettingsButtons.VOICE))
async def choice_speaker(callback: CallbackQuery, user: User):
    # if not user.tariff:
    #     await callback.answer(
    #         text="Выбор голоса для синтеза речи доступен только для пользователей с оплаченной подпиской.",
    #         show_alert=True,
    #     )
    #     return

    markup = await gen_main_speaker_kb(cur_speaker=user.tts_mode)

    await callback.message.edit_reply_markup(reply_markup=markup)
    await callback.answer()


@router.callback_query(SileroCallback.filter(F.action == SileroAction.SHOW_CATEGORY))
async def show_speaker_category(callback: CallbackQuery, callback_data: SileroCallback, user: User):
    # if not user.tariff:
    #     await callback.answer(
    #         text="Выбор голоса для синтеза речи доступен только для пользователей с оплаченной подпиской.",
    #         show_alert=True,
    #     )
    #     return

    category = callback_data.category
    subcategory = callback_data.subcategory

    markup = await gen_speaker_category_kb(cur_speaker=user.tts_mode, category=category, cur_subcategory=subcategory)

    await callback.message.edit_reply_markup(reply_markup=markup)
    await callback.answer()


@router.callback_query(SileroCallback.filter(F.action == SileroAction.SET))
async def set_speaker_handler(callback: CallbackQuery, callback_data: SileroCallback, user: User):
    speaker = None if callback_data.value == "0" else callback_data.value
    category = callback_data.category
    subcategory = callback_data.subcategory

    if user.tts_mode != speaker:
        await update_object(user, tts_mode=speaker, update_relations=True)

    if speaker is None:
        markup = await gen_txt_settings_kb(user)
    else:
        markup = await gen_speaker_category_kb(cur_speaker=user.tts_mode, category=category,
                                               cur_subcategory=subcategory)

    try:
        await callback.message.edit_reply_markup(reply_markup=markup)
    except TelegramBadRequest:
        pass
    await callback.answer()


@router.callback_query(SileroCallback.filter(F.action == SileroAction.EXAMPLE))
async def send_example(callback: CallbackQuery, user: User):
    await callback.answer("TODO", show_alert=True)  # TODO

    # example = FSInputFile(f"{settings.MEDIA_DIR}/tts_examples/{user.tts_mode}.wav")
    #
    # await callback.message.answer_voice(example, caption=user.tts_mode)
    # await callback.answer()


@router.callback_query(SileroCallback.filter(F.action == SileroAction.NONE))
async def empty_button(callback: CallbackQuery):
    await callback.answer()


@router.callback_query(ImageModelCallback.filter())
async def set_image_model(callback: CallbackQuery, callback_data: ImageModelCallback, user: User):
    if user.img_model == callback_data.model:
        pass
    else:
        await update_object(user, img_model=callback_data.model, update_relations=True)
        text = gen_img_settings_text(user)
        markup = await gen_img_model_kb(user)

        await callback.message.edit_text(text=text, reply_markup=markup)

    await callback.answer()
