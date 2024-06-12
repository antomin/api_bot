from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, LabeledPrice

from common.models import User, Tariff, db
from tgbot_app.keyboards.inline.payments_keyboards import gen_confirm_tokens_kb
from common.db_api import create_refund, get_obj_by_id, update_object, create_invoice
from tgbot_app.keyboards import gen_tokens_kb, gen_confirm_premium_kb
from tgbot_app.utils.callbacks import ProfileCallback, PaymentCallback
from tgbot_app.utils.enums import DefaultCommands, ProfileButtons, PayProvider, PaymentAction
from tgbot_app.utils.text_generators import (gen_token_text, gen_confirm_tariff_text,
                                             gen_premium_canceled_text,
                                             gen_premium_text, gen_refund_text)
from common.settings import settings

router = Router()


@router.callback_query(ProfileCallback.filter(F.action == ProfileButtons.TOKENS))
@router.message(Command(DefaultCommands.tokens.name))
async def tokens(message: Message | CallbackQuery, user: User):
    if isinstance(message, CallbackQuery):
        await message.answer()
        message = message.message

    await message.answer(text=gen_token_text(user), reply_markup=await gen_tokens_kb(user, PayProvider.ROBOKASSA),
                         disable_web_page_preview=True)


@router.callback_query(PaymentCallback.filter(F.action == PaymentAction.TOKENS))
async def premium_confirm(callback: CallbackQuery, callback_data: PaymentCallback, user: User):
    tariff = await get_obj_by_id(Tariff, callback_data.value)
    if callback_data.provider != PayProvider.STARS.value:
        text = (f"🏦 Вы оформляете покупку дополнительных <b>{tariff.token_balance} токенов</b>\n\n"
                f"🔹 Нажимая кнопку ниже, я даю согласие на регулярные списания, на обработку персональных данных и "
                f"принимаю условия <a href='{settings.DOMAIN}/offer/'>публичной оферты</a>")
        markup = await gen_confirm_tokens_kb(user=user, tariff=tariff)
        await callback.message.answer(text=text, reply_markup=markup)
    else:
        invoice = await create_invoice(user_id=user.id, mother_invoice_id=None, tariff_id=tariff.id, is_paid=False, sum=0)
        description = f"Покупка {tariff.token_balance} токенов"
        if tariff.price_stars == 0:
            tariff.price_stars = 1
        await callback.message.answer_invoice(
            title="Покупка токенов",
            description=description,
            currency="XTR",
            prices=[LabeledPrice(label=description, amount=tariff.price_stars)],
            payload=str(invoice.id),
            provider_token="381764678:TEST:87349",
        )
    await callback.answer()
