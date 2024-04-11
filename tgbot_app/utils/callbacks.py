from aiogram.filters.callback_data import CallbackData

from common.enums import ImageAction, ImageModels, TextModels
from tgbot_app.utils.enums import (AiTypeButtons, ProfileButtons, SileroAction,
                                   TextSettingsButtons)


class ProfileCallback(CallbackData, prefix="profile"):
    action: ProfileButtons


class AiTypeCallback(CallbackData, prefix="ai_type"):
    type: AiTypeButtons


class TextSettingsCallback(CallbackData, prefix="txt_settings"):
    action: TextSettingsButtons


class ImageModelCallback(CallbackData, prefix="img_model"):
    model: ImageModels


class TextModelCallback(CallbackData, prefix="txt_model"):
    model: TextModels


class RoleCallback(CallbackData, prefix="txt_role"):
    role_id: int


class SileroCallback(CallbackData, prefix="silero"):
    action: SileroAction
    category: str = "0"
    subcategory: str = "0"
    value: str = "0"


class MJCallback(CallbackData, prefix="mj"):
    action: ImageAction
    index: int
    task_id: str
