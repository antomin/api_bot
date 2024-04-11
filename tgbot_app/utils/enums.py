from enum import Enum

from tgbot_app.services.neiro_api import ResponseResult


class MainButtons(str, Enum):
    PROFILE = "👨‍💼 Профиль"
    AIS = "🤖 Нейросети"
    SUBSCRIPTION = "💎 Подписка"
    SERVICES = "📲 Сервисы"
    FAQ = "❓ Часто задаваемые вопросы"


class DefaultCommands(Enum):
    start = "Перезапуск 🚀"
    profile = "Профиль 👨‍💼"
    subscription = "Подписка 💳"
    tokens = "Токены 💎"
    ais = "Нейросети 🤖"
    services = "Сервисы 📲"
    faq = "Помощь ❓"


class ProfileButtons(Enum):
    AIS = "🤖 Нейросети"
    PREMIUM = "💳 Премиум"
    TOKENS = "💎 Купить Токены"


class AiTypeButtons(Enum):
    TEXT = "🔤 Генерация текста"
    IMAGE = "🏞 Генерация изображений"
    VIDEO = "🎞 Генерация видео"
    MUSIC = "🎼 Генерация музыки"


class TextSettingsButtons(Enum):
    MODEL = "model"
    VOICE = "voice"
    ROLE = "role"
    CONTEXT = "context"
    BACK = "back"


class SileroAction(Enum):
    SHOW_CATEGORY = "show_category"
    SHOW_CATEGORY_STATE = "show_category_state"
    SET = "set"
    EXAMPLE = "example"
    NONE = "none"
    BACK_TO_SERVICE = "back_to_service"
    SET_STATE = "set_state"
    START_SERVICE = "start_state"


class GenerationResult(ResponseResult):
    task_id: str | int | None = None
