from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot_app.utils.callbacks import (DiplomaCallback, LearningCallback,
                                       ServicesCallback)
from tgbot_app.utils.enums import (DiplomaAction, DiplomaStructButtons,
                                   LearningButtons, ServicesButtons, WorkTypes)


async def gen_type_work_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for work_type in WorkTypes:
        builder.button(text=work_type.value,
                       callback_data=DiplomaCallback(action=DiplomaAction.SET_TYPE, value=work_type.name.lower()))

    builder.button(text="↩️ Назад", callback_data=ServicesCallback(type=ServicesButtons.LEARN))

    return builder.adjust(1).as_markup()


async def gen_diploma_struct_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="🪄 Начать генерацию", callback_data=DiplomaCallback(action=DiplomaAction.CONFIRM))
    builder.button(text="🗓 Задать план", callback_data=DiplomaCallback(action=DiplomaAction.GET_STRUCT))
    builder.button(text="↩️ Назад", callback_data=LearningCallback(type=LearningButtons.WORKS))

    return builder.adjust(2, 1).as_markup()


async def gen_confirm_start_work_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Да", callback_data=DiplomaCallback(action=DiplomaAction.START))
    builder.button(text="❌Нет", callback_data="back_to_services")

    return builder.adjust(2).as_markup()
