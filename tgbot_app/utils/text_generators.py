from common.db_api import get_obj_by_id
from common.enums import ImageModels, TextModels
from common.models import Tariff, User
from common.settings import settings
from tgbot_app.utils.misc import decl


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
        text += (
            f"├ Ваши токены: {user.token_balance}\n"
            f"├ {user.gemini_daily_limit} из {settings.FREE_GEMINI_QUERIES} генераций Gemini Pro\n"
            f"├ {user.sd_daily_limit} из  {settings.FREE_SD_QUERIES} генераций StableDiffusion\n"
            f"└ {user.kandinsky_daily_limit} из {settings.FREE_KANDINSKY_QUERIES} генераций Kandinsky\n\n"
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

    if user.txt_model == TextModels.GEMINI:
        if not user.tariff:
            text += (
                f"{settings.MODELS[user.txt_model].cost} токена\n"
                f"├ У вас осталось {user.gemini_daily_limit} ежедневных запросов\n"
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

    if not user.tariff_id and user.img_model == ImageModels.KANDINSKY:
        num = user.kandinsky_daily_limit  # if user.img_model == ImageModels.KANDINSKY else user.sd_daily_limit
        text += f"\n└ У вас осталось {num} ежедневных запросов"

    return text


async def gen_confirm_tariff_text(tariff: Tariff) -> str:
    if tariff.is_trial:
        main_tariff = await get_obj_by_id(Tariff, tariff.main_tariff_id)
        text = (f"💳 Вы оформляете ПРОБНЫЙ тариф за {tariff.price}₽ <b>на {tariff.days} дня</b>. Он предоставит Вам "
                f"{tariff.token_balance} токенов. Если Вы не откажитесь от него (это можно сделать), то тариф "
                f"автоматически продлится за {main_tariff.price}₽ еще на {main_tariff.days} дней по "
                f"которому Вам будет предоставлено уже {main_tariff.token_balance} токенов.")
    else:
        text = (f"💳 Вы оформляете тариф за {tariff.price}₽. Он предоставит Вам {tariff.token_balance} токенов на "
                f"{tariff.days} дней, а стоимость токенов уменьшится в 2 раза.")

    text += (f"\n\nНажимая кнопку ниже, я даю согласие на дальнейшие списания, а также на обработку персональных "
             f"данных и принимаю условия <a href='{settings.DOMAIN}/offer/'>публичной оферты</a>.")

    return text


def gen_refund_text(can_refund: bool) -> str:
    text = "💳 <b>Хотите отказаться от подписки? </b>\n"

    if can_refund:
        text += ("При отказе от подписки, Вам будет сделан возврат средств, Ваши токены будут аннулированы, а все "
                 "токены купленные по подписки поделены на два. Возврат средств происходит через платежный агрегатор "
                 "Robokassa. В течении 2-х дней Вам придет уведомление о создании заявки на возврат средств на "
                 "почту с которой вы производили оплату. Возврат средств может быть очень быстрый, но в редких "
                 "случаях нужно ожидать от 7 до 30 банковских дней.")
    else:
        text += "Ваша подписка будет действовать до конца оплаченного срока, но возврат средств сделать уже нельзя."

    text += (f' Согласно <a href="{settings.DOMAIN}/offer/">договору оферты</a>, с которым Вы согласились при '
             f"оформлении подписки, у Вас есть 48 часов для возврата средств.")

    return text


def gen_premium_canceled_text(can_refund: bool) -> str:
    text = "Нам очень жаль что вы отказались от подписки, надеемся вы вернетесь к нам снова!"
    if can_refund:
        text += ("\n\nСредства будут автоматически возвращены Вам обратно на карту, с которой вы производили оплату. "
                 "Срок возврата от 1 часа до 7 рабочих дней.")

    return text


def gen_token_text(user: User) -> str:
    text = (f"💎 <b>Токены</b>\nвиртуальная валюта, которой ты можешь оплачивать свои запросы в нейросетях.\n\n"
            f"Нажимая кнопку ниже, я даю согласие на обработку персональных данных и принимаю условия "
            f"<a href='{settings.DOMAIN}/offer/'>публичной оферты</a>.")

    if not user.tariff or user.tariff.is_trial:
        text += "❤️‍🔥С премиум подпиской стоимость токенов будет в 2 раза дешевле."

    return text
