from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from common.settings import settings
from tgbot_app.utils.callbacks import AdminCallback, AdminLinksCallback
from tgbot_app.utils.enums import AdminLinksButtons, AdminMainButtons


async def gen_admin_main_kb(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    report_webapp = WebAppInfo(url=f"{settings.DOMAIN}/reports/current/{user_id}/")

    for btn in AdminMainButtons:
        builder.button(text=btn.value, callback_data=AdminCallback(chapter=btn))
    # builder.button(text="Статистика", web_app=report_webapp)

    return builder.adjust(1).as_markup()


async def gen_admin_links_kb(profile_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    static_webapp = WebAppInfo(url=f"{settings.DOMAIN}/reports/links/{profile_id}/")

    builder.button(text=AdminLinksButtons.CREATE.value,
                   callback_data=AdminLinksCallback(command=AdminLinksButtons.CREATE))
    builder.button(text="Статистика", web_app=static_webapp)

    return builder.adjust(2).as_markup()
