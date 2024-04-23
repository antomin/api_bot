from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from common.db_api import create_object, update_object
from common.models import ReferalLink, User
from common.settings import settings
from tgbot_app.keyboards import gen_admin_links_kb, gen_admin_main_kb
from tgbot_app.utils.callbacks import AdminCallback, AdminLinksCallback
from tgbot_app.utils.enums import AdminLinksButtons, AdminMainButtons
from tgbot_app.utils.states import CommonState

router = Router()


@router.message(F.text == "⚒️ Панель администратора")
async def start_admin(message: Message, user: User, state: FSMContext):
    if not user.is_admin:
        return

    await state.clear()

    await message.answer(text="Выберите действие:", reply_markup=await gen_admin_main_kb(user.id))


@router.callback_query(AdminCallback.filter(F.chapter == AdminMainButtons.LINKS))
async def admin_links(callback: CallbackQuery, user: User):
    if not user.is_admin:
        return

    await callback.message.answer(text="Раздел ссылок:", reply_markup=await gen_admin_links_kb(user.id))
    await callback.answer()


@router.callback_query(AdminLinksCallback.filter(F.command == AdminLinksButtons.CREATE))
async def admin_links_get_name(callback: CallbackQuery, user: User, state: FSMContext):
    if not user.is_admin:
        return

    await callback.message.answer("Введите название ссылки:")
    await callback.answer()

    await state.set_state(CommonState.LINK)


@router.message(CommonState.LINK)
async def admin_links_create(message: Message, user: User, state: FSMContext):
    if not user.is_admin:
        return

    name = message.text
    link = await create_object(ReferalLink, name=name, owner_id=user.id)
    bot_link = f"https://t.me/{settings.BOT_USERNAME}?start={link.id}"
    site_link = f"{settings.DOMAIN}/redirect/{link.id}/"
    await update_object(link, bot_link=bot_link, site_link=site_link)

    text = f"Ваши ссылки <b>{name}</b>:\n\n<code>{bot_link}</code>\n<code>{site_link}</code>"

    await message.answer(text)

    await state.clear()
