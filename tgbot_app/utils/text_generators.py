from common.db_api import get_obj_by_id
from common.enums import ImageModels, TextModels
from common.models import Tariff, User, Report
from common.settings import settings
from tgbot_app.utils.misc import decl


async def gen_profile_text(user: User) -> str:
    tariff: Tariff = user.tariff

    if not tariff:
        tariff_str = "Free"
    elif tariff.is_trial:
        tariff_str = "TRIAL"
    else:
        tariff_str = f"PREMIUM {tariff.token_balance}"

    text = f'👨‍💻 <b>Добро пожаловать</b>{(", " + user.first_name) if user.first_name else "<b>!</b>"}\n'
    if user.username:
        text += f"├ Ваш юзернейм: <code>@{user.username}</code>\n"
    text += f"└ Ваш ID: <code>{user.id}</code>\n\n"

    if not tariff:
        text += (f"Каждый день вам даются бесплатные генерации изображений через нейросеть Kandinsky и бесплатные "
                 f"запросы в Gemini (аналог ChatGPT от Google).\n\n"
                 f"💳 Подписка: <b>{tariff_str}</b>\n"
                 f"├ Ваши токены: {user.token_balance}\n"
                 f"├ {user.gemini_daily_limit} из {settings.FREE_GEMINI_QUERIES} генераций Gemini\n"
                 f"└ {user.kandinsky_daily_limit} из {settings.FREE_KANDINSKY_QUERIES} генераций Kandinsky\n\n"
                 f"<i>* Ваши бесплатные генерации обновятся "
                 f"{user.update_daily_limits_time.strftime('%d-%m-%Y %H:%M')} МСК.</i>")
    else:
        words, time_left = user.sub_time_left()
        time_left_str = f"{time_left} {decl(time_left, words)}"

        text += (f"💳 Подписка: <b>{tariff_str}</b>\n"
                 f"├ Подписка истекает через: {time_left_str}\n"
                 f"├ Кол-во токенов по подписке: {tariff.token_balance} токенов\n"
                 f"├ Текущие кол-во токенов: {user.token_balance}\n"
                 f"├ Безлимит Kandinsky\n"
                 f"└ Безлимит ChatGPT 3.5 + Gemini")

    return text


def gen_txt_settings_text(user: User) -> str:
    model = settings.MODELS[user.txt_model]
    text = (f"🔹 Вы можете задавать вопросы голосом и получать озвученные ответы, а также изменять версии модели. "
            f"Стоимость запроса зависит от выбранной нейросети и ее модели. В данный момент у вас выбрана модель "
            f"{model.name}. {model.desc}\n\n💎 Стоимость: ")

    if user.txt_model in (TextModels.GEMINI, TextModels.GPT_3_TURBO):
        if not user.tariff:
            text += f"{model.cost} токена\n"
            if user.txt_model == TextModels.GEMINI:
                text += f"├ У вас осталось {user.gemini_daily_limit} из {settings.FREE_GEMINI_QUERIES}\n"
            text += f"└ При наличии подписки генерации {model.name} для вас будут безлимитными."

        else:
            text += "Безлимит по подписке"
    else:
        text += f"{model.cost} токенов"

    return text


def gen_img_settings_text(user: User) -> str:
    model = settings.MODELS[user.img_model]
    text = (f"🔹 Выберите одну из предложенных нейросетей. В данный момент генерация будет происходить при помощи "
            f"{model.name}. {model.desc}\n\n⚠️ <i>Стоит обратить внимание!")

    if user.img_model in (ImageModels.MIDJOURNEY, ImageModels.DALLE_3):
        text += "\n├ Не отправляйте запрос с эротикой и жестью в любом виде, запрос будет отменен.\n"
        if user.img_model == ImageModels.MIDJOURNEY:
            text += ("├ Рекомендуем писать запросы на английском, так нейросеть выдает более точные генерации.\n"
                     "└ <a href='https://telegra.ph/Kak-ukazat-versiyu-Midjourney-dlya-generacii-04-25'>Инструкция "
                     "для продвинутых пользователей</a></i>")
        else:
            text += "└ Рекомендуем писать запросы на английском, так нейросеть выдает более точные генерации.</i>"
    else:
        text += " Не отправляйте запрос с эротикой и жестью в любом виде, запрос будет отменен.</i>"

    text += "\n\n💎 Стоимость: "

    if user.img_model == ImageModels.KANDINSKY:
        if not user.tariff:
            text += (f"{model.cost} токена\n"
                     f"├ {user.kandinsky_daily_limit} из {settings.FREE_KANDINSKY_QUERIES} генераций Kandinsky\n"
                     f"└ При наличии подписки генерации Kandinsky для вас будут безлимитными.")
        else:
            text += "Безлимит по подписке"
    else:
        text += f"{model.cost} токенов"

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
    text = f"💎 Токены\nвиртуальная валюта, которой ты можешь оплачивать свои запросы в нейросетях.\n\n"

    if not user.tariff or user.tariff.is_trial:
        text += ("🔥 С активной подпиской Вы сможете покупать токены <b>в 2 раза дешевле</b> указанной цены и получите "
                 "<b>безлимит на генерации</b> ChatGPT 3.5, Gemini и Kandinsky. Чтобы приобрести премиум подписку "
                 "нажмите на «⚡ Тарифы и токены»  -> «💳 Премиум»")
    else:
        text += "🔥 В данный момент у Вас есть активная подписка. Цена токенов для вас <b>снижена в 2 раза</b>!"

    text += (f"\n\nНажимая кнопку ниже, я даю согласие на обработку персональных данных и принимаю условия "
             f"<a href='{settings.DOMAIN}/offer/'>публичной оферты</a>.")

    return text


def gen_premium_text(user: User) -> str:
    text = "💳 Премиум подписка\n\n"

    if not user.tariff or user.tariff.is_trial:
        text += ("💳 <b>У Вас сейчас нет активной подписки</b>\n\n"
                 "После приобретения премиум подписка действует 30 дней. Помимо доступа к дополнительным нейросетям, "
                 "с подпиской Вы сможете использовать ChatGPT 3.5, Gemini и Kandinsky безлимитно.\n\n"
                 "💸 Токены с подпиской стоят в 2 раза дешевле. Выбирайте понравившуюся:")
    else:
        text += (f"💳 <b>У Вас сейчас активна подписка PREMIUM {user.tariff.token_balance}</b>\n\n"
                 f"Премиум подписка действует 30 дней. Помимо доступа к дополнительным нейросетям, Вы можете "
                 f"использовать ChatGPT 3.5, Gemini и Kandinsky безлимитно.\n\n"
                 f"💸 Токены с подпиской стоят в 2 раза дешевле.")

    return text


def gen_report_text(report: Report) -> str:
    text = (
        f"👥 <b>Пользователи:</b>\n"
        f"├ Всего: {report.users_cnt}\n"
        f"└ Реф. ссылки: {report.users_with_link_cnt}\n\n"
        f"📈 <b>Новые за сутки:</b>\n"
        f"├ Всего: {report.new_users_cnt}\n"
        f"├ С реф. ссылок: {report.new_users_with_link_cnt}\n"
        f"└ С поиска: {report.new_users_from_search_cnt}\n\n"
        f"🏃 <b>Статистика за сутки по нейросетям:</b>\n"
        f"├ Всего запросов: {report.queries_cnt}\n"
        f"├ ChatGPT 3.5: {report.queries_gpt_3_turbo_cnt}\n"
        f"├ ChatGPT 4 turbo: {report.queries_gpt_4_turbo_cnt}\n"
        f"├ ЯндексGPT: {report.queries_yagpt_cnt}\n"
        f"├ ЯндексGPT Lite: {report.queries_yagpt_lite_cnt}\n"
        f"├ Gemini: {report.queries_gemini_cnt}\n"
        f"├ Claude: {report.queries_claude_cnt}\n"
        f"├ StableDiffusion: {report.queries_sd_cnt}\n"
        f"├ DallE-2: {report.queries_dalle_2_cnt}\n"
        f"├ DallE-3: {report.queries_dalle_3_cnt}\n"
        f"├ Midjourney: {report.queries_mj_cnt}\n"
        f"├ Kandinsky: {report.queries_kandinsky_cnt}\n"
        f"├ Текст в видео: {report.txt_to_video_cnt}\n"
        f"├ Изображение в видео: {report.img_to_video_cnt}\n"
        f"├ Удаление фона видео: {report.rembg_cnt}\n"
        f"├ Видео в мульт: {report.cartoon_video_cnt}\n"
        f"└ PicaArt: {report.pica_video_cnt}\n\n"
        f"👨‍🎓 <b>Статистика за сутки по сервисам:</b>\n"
        f"├ Для учебы: {report.diploma_cnt + report.rewrite_cnt + report.vision_cnt}\n"
        f"│ ├ Генерация работ: {report.diploma_cnt}\n"
        f"│ ├ Рерайтинг: {report.rewrite_cnt}\n"
        f"│ └ Решение по фото: {report.vision_cnt}\n"
        f"├ Для работы: {report.articles_cnt}\n"
        f"│ └ Генерация статьи: {report.articles_cnt}\n"
        f"├ Другие: {report.tts_cnt + report.stt_cnt + report.rembg_cnt}\n"
        f"│ ├ Текст в речь: {report.tts_cnt}\n"
        f"│ ├ Речь в текст: {report.stt_cnt}\n"
        f"└─┴ Удаление фона: {report.rembg_cnt}\n\n"
        f"💰 <b>Платежи за сутки:</b>\n"
        f"├ Всего активных подписок: {report.prem_users_cnt}\n"
        f"├ Новых подписок: {report.new_prem_invoices_cnt}шт на сумму {report.new_prem_invoices_sum}₽\n"
        f"├ Продаж токенов: {report.new_token_invoices_cnt}шт на сумму {report.new_token_invoices_sum}₽\n"
        f"├ Всего: {report.new_invoices_cnt} платежей\n"
        f"├ Общий оборот: {report.new_invoices_sum}\n"
        f"├ Средний чек: {report.avg_bill}\n"
    )

    for price, count in report.tariffs_buys_dict.items():
        text += f"├ Покупок за {price}₽: {count}\n"

    text += f"└ Продлений: {report.recurring_invoices_cnt}"

    return text
