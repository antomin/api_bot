from common.db_api import get_obj_by_id
from common.models import User, Tariff


def decl(num: int, titles: tuple) -> str:
    cases = [2, 0, 1, 1, 1, 2]
    if 4 < num % 100 < 20:
        idx = 2
    elif num % 10 < 5:
        idx = cases[num % 10]
    else:
        idx = cases[5]
    return titles[idx]


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
