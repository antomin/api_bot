from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from common.db_api import get_tariffs
from common.models import Tariff, User
from common.settings import settings
from tgbot_app.utils.callbacks import PaymentCallback, ProfileCallback, PayProviderCallback
from tgbot_app.utils.enums import PaymentAction, ProfileButtons, TariffCode
from tgbot_app.utils.enums import PayProvider


async def gen_no_tokens_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="💎 Купить токенов", callback_data=ProfileCallback(action=ProfileButtons.TOKENS))
    builder.button(text="💳 Оформить подписку", callback_data=ProfileCallback(action=ProfileButtons.PREMIUM))

    return builder.adjust(1).as_markup()

def gen_price_str(user: User, tariff: Tariff, provider: PayProvider) -> str:
    price_fields = {PayProvider.ROBOKASSA: "price", PayProvider.STARS: "price_stars"}
    price = getattr(tariff, price_fields[provider])

    if price == 0:
        price = 1

    if tariff.is_extra and user.tariff.code != TariffCode.FREE and price != 1:
        price = int(price / 2)

    # if provider == PayProvider.ROBOKASSA:
    #     return f"{price}₽"
    # else:
    return f"{price}⭐"


async def gen_premium_kb(user: User, provider: PayProvider) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if not user.tariff:
        tariffs = await get_tariffs(is_trial=user.first_payment)

        for tariff in tariffs:
            price_str = gen_price_str(user=user, tariff=tariff, provider=provider)

            text = f"💳 {tariff.name} / {price_str}"
            builder.button(
                text=text,
                callback_data=PaymentCallback(action=PaymentAction.SUBSCRIBE, value=tariff.id, provider=provider),
            )

        # builder.button(text=("✅ " if provider == PayProvider.ROBOKASSA else "") + "Оплата картами РФ 🇷🇺",
        #                callback_data=PayProviderCallback(provider=PayProvider.ROBOKASSA, source="premium"))
        builder.button(text="✅ " + "Оплата Telegram STARS ⭐️",
                       callback_data=PayProviderCallback(provider=PayProvider.STARS, source="premium"))

    else:
        if not user.recurring:
            builder.button(
                text="Возобновить подписку",
                callback_data=PaymentCallback(action=PaymentAction.REACTIVATE, value=False),
            )
        else:
            builder.button(
                text="Отказаться от подписки",
                callback_data=PaymentCallback(action=PaymentAction.CANCEL, value=False),
            )

    return builder.adjust(1).as_markup()


async def gen_confirm_premium_kb(user: User, tariff: Tariff) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"Оплатить {tariff.price}₽",
        web_app=WebAppInfo(url=f"{settings.DOMAIN}/payments/redirect/{tariff.id}/{user.id}/"))

    return builder.as_markup()


async def gen_premium_cancel_kb(refund: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="❌ Отказаться от подписки",
                   callback_data=PaymentCallback(action=PaymentAction.CONFIRM_CANCEL, value=refund))
    builder.button(text="✅ Вернуться в меню", callback_data="start")

    return builder.adjust(1).as_markup()


async def gen_tokens_kb(user: User, provider: PayProvider) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    tariffs = await get_tariffs(is_extra=True)

    for tariff in tariffs:
        price_str = gen_price_str(user=user, tariff=tariff, provider=provider)
        text = f"💎 {tariff.name} / {price_str}"
        builder.button(
            text=text,
            callback_data=PaymentCallback(action=PaymentAction.TOKENS, value=tariff.id, provider=provider),
        )

    # builder.button(text=("✅ " if provider == PayProvider.ROBOKASSA else "") + "Оплата картами РФ 🇷🇺",
    #                callback_data=PayProviderCallback(provider=PayProvider.ROBOKASSA, source="tokens"))
    builder.button(text="✅ " + "Оплата Telegram STARS ⭐️",
                   callback_data=PayProviderCallback(provider=PayProvider.STARS, source="tokens"))

    return builder.adjust(1).as_markup()


async def gen_confirm_tokens_kb(user: User, tariff: Tariff) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"Оплатить {tariff.price}₽",
        web_app=WebAppInfo(url=f"{settings.DOMAIN}/payments/redirect/{tariff.id}/{user.id}/"))

    return builder.as_markup()
