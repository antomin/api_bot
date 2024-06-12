from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, LabeledPrice, PreCheckoutQuery, ContentType
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select
from asgiref.sync import sync_to_async

from common.db_api import create_refund, get_obj_by_id, update_object, create_invoice, async_update_subscription
from common.models import Tariff, User, Invoice, db
from tgbot_app.keyboards import (gen_confirm_premium_kb, gen_premium_cancel_kb,
                                 gen_premium_kb, main_kb, gen_tokens_kb)
from tgbot_app.utils.callbacks import PaymentCallback, ProfileCallback, PayProviderCallback
from tgbot_app.utils.enums import (DefaultCommands, PaymentAction,
                                   ProfileButtons, PayProvider)
from tgbot_app.utils.misc import can_create_refund
from tgbot_app.utils.text_generators import (gen_confirm_tariff_text,
                                             gen_premium_canceled_text,
                                             gen_premium_text, gen_refund_text)
from tgbot_app.handlers.profile_handler import gen_profile_text, gen_profile_kb
from tgbot_app.utils.text_variables import REACTIVATE_RECURRING_TEXT
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(Command(DefaultCommands.subscription.name))
@router.callback_query(ProfileCallback.filter(F.action == ProfileButtons.PREMIUM))
async def premium_handler(message: Message | CallbackQuery, user: User):
    if isinstance(message, CallbackQuery):
        await message.answer()
        message = message.message

    await message.answer(text=gen_premium_text(user), reply_markup=await gen_premium_kb(user, PayProvider.ROBOKASSA))


@router.callback_query(PaymentCallback.filter(F.action == PaymentAction.SUBSCRIBE))
async def premium_confirm(callback: CallbackQuery, callback_data: PaymentCallback, user: User):
    tariff = await get_obj_by_id(Tariff, callback_data.value)
    if callback_data.provider != PayProvider.STARS.value:
        await callback.message.answer(text=await gen_confirm_tariff_text(tariff),
                                      reply_markup=await gen_confirm_premium_kb(user=user, tariff=tariff),
                                      disable_web_page_preview=True)
        await callback.answer()
    else:
        invoice = await create_invoice(user_id=user.id, mother_invoice_id=None, tariff_id=tariff.id, is_paid=False, sum=0)
        description = f"Оплата подписки PREMIUM {tariff.token_balance}"
        if tariff.price_stars == 0:
            tariff.price_stars = 1
        await callback.message.answer_invoice(
            title="Покупка тарифа",
            description=description,
            currency="XTR",
            prices=[LabeledPrice(label=description, amount=tariff.price_stars)],
            payload=str(invoice.id),
            provider_token="381764678:TEST:87349",
        )
    await callback.answer()


@router.pre_checkout_query()
async def pre_checkout_handler(query: PreCheckoutQuery):
    inv_id = int(query.invoice_payload)
    async with db.async_session_factory() as session:
        # Выполняем запрос на загрузку объекта Invoice с жадной загрузкой связанного профиля
        stmt = select(Invoice).options(joinedload(Invoice.user), joinedload(Invoice.tariff)).where(Invoice.id == inv_id)
        result = await session.execute(stmt)
        invoice = result.scalars().first()

        if invoice:
            invoice.is_paid = True
            await session.commit()  # Сохраняем изменения в базе данных
            await async_update_subscription(user=invoice.user, tariff=invoice.tariff, invoice=invoice, session=session)

            await query.answer(ok=True)


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def success_payment_handler(message: Message, user: User):
    text = await gen_profile_text(user)
    markup = await gen_profile_kb()
    await message.answer(text=text, reply_markup=markup)


async def premium_cancel(callback: CallbackQuery, user: User):
    can_refund = await can_create_refund(user)

    await callback.message.answer(text=gen_refund_text(await can_create_refund(user)),
                                  reply_markup=await gen_premium_cancel_kb(refund=can_refund),
                                  disable_web_page_preview=True)
    await callback.answer()


@router.callback_query(PaymentCallback.filter(F.action == PaymentAction.CONFIRM_CANCEL))
async def premium_cancel_confirm(callback: CallbackQuery, callback_data: PaymentCallback, user: User):
    refund = bool(callback_data.value)

    text = gen_premium_canceled_text(refund)
    markup = await main_kb(user)

    if refund:
        await create_refund(user)
    else:
        await update_object(user, recurring=False)

    await callback.message.answer(text=text, reply_markup=markup)
    await callback.answer()


@router.callback_query(PaymentCallback.filter(F.action == PaymentAction.REACTIVATE))
async def reactivate_recurring(callback: CallbackQuery, user: User):

    await update_object(user, recurring=True)

    await callback.message.answer(text=REACTIVATE_RECURRING_TEXT, reply_markup=await main_kb(user))
    await callback.answer()


@router.callback_query(PayProviderCallback.filter())
async def toggle_provider(callback: CallbackQuery, callback_data: PayProviderCallback, user: User, state: FSMContext):
    provider = callback_data.provider
    await state.update_data({"provider": provider})
    if callback_data.source == "premium":
        markup = await gen_premium_kb(user=user, provider=provider)
    elif callback_data.source == "tokens":
        markup = await gen_tokens_kb(user=user, provider=provider)
    else:
        markup = None

    try:
        await callback.message.edit_reply_markup(reply_markup=markup)
    except TelegramBadRequest:
        pass
    await callback.answer()
