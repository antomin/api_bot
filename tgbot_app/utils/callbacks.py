from aiogram.filters.callback_data import CallbackData

from tgbot_app.utils.enums import ProfileButtons


class ProfileCallback(CallbackData, prefix="profile"):
    action: ProfileButtons
