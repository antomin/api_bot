from aiogram import F, Router
from aiogram.types import CallbackQuery

from tgbot_app.utils.callbacks import OtherServicesCallback
from tgbot_app.utils.enums import OtherServicesButtons
from tgbot_app.utils.text_variables import RECONSTRUCTION_TEXT

router = Router()


@router.callback_query(OtherServicesCallback.filter(F.type == OtherServicesButtons.REMOVE_BACK))
async def img_rembg_handler(callback: CallbackQuery):
    await callback.answer(text=RECONSTRUCTION_TEXT, show_alert=True)
