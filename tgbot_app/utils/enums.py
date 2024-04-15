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


class ServicesButtons(Enum):
    LEARN = "👨‍🎓 Для учёбы"
    WORK = "👨‍💻 Для работы"
    OTHER = "📱 Другие сервисы"


class LearningButtons(Enum):
    WORKS = "📄 Генерация работ"
    ANTIPLAGIARISM = "✍️ Повышение уникальности"
    PHOTO = "📸 Решение по фото"


class WorkingButtons(Enum):
    MARKETING = "🚧 Маркетологам"
    SMM = "🚧 SMM специалистам"
    SEO = "SEO специалистам"
    COPYRIGHT = "Копирайтерам"


class OtherServicesButtons(Enum):
    TTS = "🔉 Текст в речь"
    STT = "🎤 Речь в текст"
    REMOVE_BACK = "🏙 Удаление фона"


class WorkTypes(Enum):
    ESSAY = "✏️ Эссе"
    DIPLOMA = "📚 Дипломная работа"
    COURSEWORK = "😮‍💨 Курсовая работа"
    REPORT = "📝 Реферат"


class DiplomaAction(Enum):
    SET_TYPE = "set_type"
    STRUCT = "struct"
    GET_STRUCT = "get_struct"
    CONFIRM = "confirm"
    START = "start"


class DiplomaStructButtons(Enum):
    START_GEN = "🪄 Начать генерацию"
    GET_STRUCT = "🗓 Задать план"


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
