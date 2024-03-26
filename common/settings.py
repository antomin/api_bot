from dataclasses import dataclass
from pathlib import Path

from environs import Env
from pydantic_settings import BaseSettings

from common.enums import ImageModels, TextModels

env = Env()
env.read_env("../.env")

_db_host: str = env.str("DB_HOST")
_db_port: int = env.int("DB_PORT")
_db_name: str = env.str("DB_NAME")
_db_user: str = env.str("DB_USER")
_db_pass: str = env.str("DB_PASS")


@dataclass
class Model:
    name: str
    cost: int


models_data = {
    TextModels.GPT_3_TURBO: Model(name="ChatGPT 3.5 Turbo", cost=env.int("COST_GPT_3")),
    TextModels.GPT_4_TURBO: Model(name="ChatGPT 4 Turbo", cost=env.int("COST_GPT_4")),
    TextModels.YAGPT: Model(name="Яндекс GPT", cost=env.int("COST_YAGPT")),
    TextModels.YAGPT_LITE: Model(name="Яндекс GPT Lite", cost=env.int("COST_YAGPT_LITE")),
    TextModels.CLAUDE: Model(name="Claude", cost=env.int("COST_CLAUDE")),
    TextModels.GEMINI: Model(name="Gemini", cost=env.int("COST_GEMINI")),

    ImageModels.STABLE_DIFFUSION: Model(name="Stable Diffusion", cost=env.int("COST_SD")),
    ImageModels.MIDJOURNEY: Model(name="Midjourney", cost=env.int("COST_MIDJOURNEY")),
    ImageModels.DALLE_2: Model(name="Dall-E 2", cost=env.int("COST_DALLE2")),
    ImageModels.DALLE_3: Model(name="Dall-E 3", cost=env.int("COST_DALLE3")),
    ImageModels.KANDINSKY: Model(name="Kandinsky", cost=env.int("COST_KANDINSKY")),
}


class Settings(BaseSettings):
    DEBUG: bool = env.bool("DEBUG")
    SECRET_KEY: str = env.str("SECRET_KEY")

    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    MEDIA_DIR: Path = BASE_DIR / "tgbot_app" / "media"

    APP_NAME: str = env.str("APP_NAME")
    DOMAIN: str = env.str("DOMAIN")

    TG_TOKEN: str = env.str("TG_TOKEN")
    BOT_USERNAME: str = env.str("BOT_USERNAME")
    SUPPORT_USERNAME: str = env.str("SUPPORT_USERNAME")
    TARGET_CHAT: str = env.str("TARGET_CHAT")

    NEIRO_TOKEN: str = env.str("NEIRO_TOKEN")

    ROBOKASSA_LOGIN: str = env.str("ROBOKASSA_LOGIN")
    ROBOKASSA_PASS1: str = env.str("ROBOKASSA_PASS1")
    ROBOKASSA_PASS2: str = env.str("ROBOKASSA_PASS2")

    DB_URL: str = f"postgresql+psycopg2://{_db_user}:{_db_pass}@{_db_host}:{_db_port}/{_db_name}"
    ASYNC_DB_URL: str = f"postgresql+asyncpg://{_db_user}:{_db_pass}@{_db_host}:{_db_port}/{_db_name}"
    REDIS_URL: str = env.str("REDIS_URL")

    FREE_GPT_QUERIES: int = env.int("FREE_GPT_QUERIES")
    FREE_SD_QUERIES: int = env.int("FREE_SD_QUERIES")
    FREE_DALLE2_QUERIES: int = env.int("FREE_DALLE2_QUERIES")

    MODELS: dict[str, Model] = models_data


settings = Settings()
