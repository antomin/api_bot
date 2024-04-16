import os

from aiogram import Bot
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.types import Message

from common.db_api import get_messages, get_obj_by_id
from common.enums import ImageModels, TextModels, VideoModels
from common.models import Tariff, User
from common.settings import settings
from tgbot_app.keyboards import gen_error_kb, gen_no_tokens_kb
from tgbot_app.services import neiro_api, translator
from tgbot_app.utils.text_variables import (ERROR_STT_TEXT,
                                            ERROR_TRANSLATION_TEXT)


def decl(num: int, titles: tuple) -> str:
    cases = [2, 0, 1, 1, 1, 2]
    if 4 < num % 100 < 20:
        idx = 2
    elif num % 10 < 5:
        idx = cases[num % 10]
    else:
        idx = cases[5]
    return titles[idx]


def delete_file(path: str) -> None:
    try:
        os.remove(path)
    except:
        pass


async def gen_profile_text(user: User) -> str:
    tariff: Tariff = user.tariff

    if not tariff:
        tariff_str = "Free"
    elif tariff.is_trial:
        main_tariff: Tariff = await get_obj_by_id(Tariff, tariff.main_tariff_id)
        tariff_str = f"Trial {main_tariff.token_balance}"
    else:
        tariff_str = f"PREMIUM {tariff.token_balance}"

    text = f'👨‍💻 <b>Добро пожаловать</b>{(", " + user.first_name) if user.first_name else "<b>!</b>"}\n'
    if user.username:
        text += f"├ Ваш юзернейм: <code>@{user.username}</code>\n"
    text += f"└ Ваш ID: <code>{user.id}</code>\n\n💳 Подписка: <b>{tariff_str}</b>\n"

    if not tariff:
        chatgpt_daily_str = decl(user.chatgpt_daily_limit, ("генерация", "генерации", "генераций"))
        sd_daily_str = decl(user.sd_daily_limit, ("генерация", "генерации", "генераций"))
        dalle_2_str = decl(user.dalle_2_daily_limit, ("генерация", "генерации", "генераций"))

        text += (
            f"├ Ваши токены: {user.token_balance}\n"
            f"├ {user.chatgpt_daily_limit} {chatgpt_daily_str} ChatGPT 3.5\n"
            f"├ {user.sd_daily_limit} {sd_daily_str} StableDiffusion\n"
            f"└ {user.dalle_2_daily_limit} {dalle_2_str} Dall-E 2\n\n"
            f"<i>* Ваши бесплатные генерации обновляются каждые 24 часа.</i>"
        )
    else:
        words, time_left = user.sub_time_left()
        time_left_str = f"{time_left} {decl(time_left, words)}"

        text += (
            f"├ Подписка истекает через: <u>{time_left_str}</u>\n"
            f"├ Кол-во токенов по подписке: {tariff.token_balance} токенов\n"
            f"├ Текущие кол-во токенов: {user.token_balance}\n"
            f"└ Безлимит ChatGPT 3.5 + Синтез речи"
        )

    return text


def gen_txt_settings_text(user: User) -> str:
    text = ("🔹 Вы можете задавать вопросы голосом и получать озвученные ответы, а также изменять версии модели. "
            "Стоимость каждой модели зависит от версии ChatGPT.\n\n💎 <b>Стоимость:</b> ")

    if user.txt_model == TextModels.GPT_3_TURBO:
        if not user.tariff:
            text += (
                f"{settings.MODELS[user.txt_model].cost} токена\n"
                f"├ У вас осталось {user.chatgpt_daily_limit} ежедневных запросов\n"
                f"└ На модель ChatGPT 3.5 Turbo (это самая популярная модель) распространяется безлимит по подписке."
            )
        else:
            text += f"Безлимит по подписке"
    else:
        text += f"{settings.MODELS[user.txt_model].cost} токенов"

    return text


def gen_img_settings_text(user: User) -> str:
    text = (f"🔹 Для Вашего выбора доступно несколько популярных нейросетей Dall-E 2, Dall-E3, Stable diffusion и др. "
            f"Ежедневно мы продолжаем работать над добавлением других нейросетей для генерации изображений.\n\n"
            f"💎 <b>Стоимость:</b> {settings.MODELS[user.img_model].cost} токенов")

    if not user.tariff and user.img_model in (ImageModels.DALLE_2, ImageModels.STABLE_DIFFUSION):
        num = user.dalle_2_daily_limit if user.img_model == ImageModels.DALLE_2 else user.sd_daily_limit
        text += f"\n└ У вас осталось {num} ежедневных запросов"

    return text


def can_send_query(user: User, model: ImageModels | TextModels | VideoModels) -> bool:  # TODO Review
    model_cost = settings.MODELS[model].cost
    if not user.tariff:
        if model in (ImageModels.DALLE_2, ImageModels.STABLE_DIFFUSION, TextModels.GPT_3_TURBO):
            if model == TextModels.GPT_3_TURBO:
                return bool(user.chatgpt_daily_limit) or user.token_balance >= model_cost
            if model == ImageModels.DALLE_2:
                return bool(user.dalle_2_daily_limit) or user.token_balance >= model_cost
            if model == ImageModels.STABLE_DIFFUSION:
                return bool(user.sd_daily_limit) or user.token_balance >= model_cost
        return user.token_balance >= model_cost
    else:
        if model == TextModels.GPT_3_TURBO:
            return True
        return user.token_balance >= model_cost


async def send_no_balance_msg(user: User, bot: Bot) -> None:
    if not user.tariff:
        text = "🔒 Вам не хватает токенов для генерации! Но вы можете докупить их или оформить подписку на 30 дней."
    else:
        text = ("🔒 Похоже Вы использовали все Ваши токены, предоставленные по подписке. Но Вы можете купить еще "
                "токенов. Для Вас они будут в 2 раза дешевле.")
    markup = await gen_no_tokens_kb()
    await bot.send_message(chat_id=user.id, text=text, reply_markup=markup)
    raise CancelHandler()


async def handle_voice_prompt(message: Message, user: User) -> str:
    if not user.tariff:
        await message.answer(text="🗣️ Голосовые запросы доступны только в тарифе PREMIUM.",
                             reply_markup=await gen_no_tokens_kb())
        raise CancelHandler()

    if message.voice.duration > 30:
        await message.answer(text="🗣️ Длина аудио не должна превышать 30сек. Попробуйте ещё раз.")
        raise CancelHandler()

    path = f"{settings.MEDIA_DIR}/tmp/{user.id}.ogg"
    await message.bot.download(file=message.voice.file_id, destination=path)
    voice_url = f"{settings.DOMAIN}/tmp/{user.id}.ogg"

    result = await neiro_api.speech_to_text(voice_url)

    delete_file(path)

    if not result.success:
        await message.answer(text=ERROR_STT_TEXT, reply_markup=await gen_error_kb())
        raise CancelHandler()

    return result.result


async def gen_conversation(user: User, prompt: str) -> list[dict]:
    if user.txt_model_role_id:
        conversation = [{"role": "system", "content": user.txt_model_role.prompt}]
    else:
        conversation = [{"role": "system", "content": "You are a personal helpful assistant. Fluent Russian speaks."}]

    if user.text_session_id:
        messages = await get_messages(user.text_session_id)  # noqa
        for msg in messages:
            if msg.prompt and msg.result:
                conversation.append({"role": "user", "content": msg.prompt})
                conversation.append({"role": "assistant", "content": msg.result})

    conversation.append({"role": "user", "content": prompt})

    return conversation


async def translate_text(text: str, message: Message) -> str:
    result = await translator.translate(text)

    if result.success:
        return result.result

    await message.answer(text=ERROR_TRANSLATION_TEXT)
    raise CancelHandler()


def parse_user_work_struct(raw_struct: str) -> dict | None:
    struct = {}
    raw_lst = raw_struct.split("\n")
    cur_chapter = ""
    cur_subchapter = ""

    try:
        for row in raw_lst:
            if not row:
                continue
            if row.strip()[0] == "*":
                cur_chapter = row.replace("*", "").strip()
                struct[cur_chapter] = {}
            elif row.strip()[0] == "+":
                cur_subchapter = row.replace("+", "").strip()
                struct[cur_chapter][cur_subchapter] = []
            elif row.strip()[0] == "-":
                struct[cur_chapter][cur_subchapter].append(row.replace("-", "").strip())
            else:
                raise KeyError

    except KeyError:
        return

    return struct
