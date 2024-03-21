from enum import Enum

from pydantic import BaseModel


class DefaultCommand(BaseModel):
    command: str
    desc: str


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
