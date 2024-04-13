from typing import Any

from aiogram.filters.callback_data import CallbackData

from common.enums import ImageAction, ImageModels, TextModels, VideoModels
from tgbot_app.utils.enums import (AiTypeButtons, DiplomaAction,
                                   DiplomaStructButtons, LearningButtons,
                                   OtherServicesButtons, ProfileButtons,
                                   ServicesButtons, SileroAction,
                                   TextSettingsButtons, WorkingButtons,
                                   WorkTypes)


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


class VideoModelCallback(CallbackData, prefix="video_model"):
    model: VideoModels


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


class ServicesCallback(CallbackData, prefix="services"):
    type: ServicesButtons


class LearningCallback(CallbackData, prefix="learning"):
    type: LearningButtons


class WorkingCallback(CallbackData, prefix="working"):
    type: WorkingButtons


class OtherServicesCallback(CallbackData, prefix="o_service"):
    type: OtherServicesButtons


class DiplomaCallback(CallbackData, prefix="diploma"):
    action: DiplomaAction
    value: Any = "_"
