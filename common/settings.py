import json
from dataclasses import dataclass
from pathlib import Path

from environs import Env
from pydantic_settings import BaseSettings

from common.enums import ImageModels, ServiceModels, TextModels, VideoModels

_base_dir: Path = Path(__file__).resolve().parent.parent

env = Env()
env.read_env(f"{_base_dir}/.env")

_db_host: str = env.str("DB_HOST")
_db_port: int = env.int("DB_PORT")
_db_name: str = env.str("DB_NAME")
_db_user: str = env.str("DB_USER")
_db_pass: str = env.str("DB_PASS")


@dataclass
class Model:
    name: str
    cost: int


def get_settings():
    settings_data = {}
    with open(f"{_base_dir}/common/settings.json", "r", encoding="utf-8") as file:
        settings_raw_data = json.loads(file.read())
        
    for section, data in settings_raw_data.items():
        for key, info in data.items():
            settings_data[key] = info['value']
            
    return settings_data


settings_data = get_settings()

models_data = {
    TextModels.GPT_3_TURBO: Model(name="ChatGPT 3.5 Turbo", cost=settings_data["cost_gpt_3"]),
    TextModels.GPT_4_TURBO: Model(name="ChatGPT 4 Turbo", cost=settings_data["cost_gpt_4"]),
    TextModels.YAGPT: Model(name="Яндекс GPT", cost=settings_data["cost_yagpt"]),
    TextModels.YAGPT_LITE: Model(name="Яндекс GPT Lite", cost=settings_data["cost_yagpt_lite"]),
    TextModels.CLAUDE: Model(name="Claude", cost=settings_data["cost_claude"]),
    TextModels.GEMINI: Model(name="Gemini", cost=settings_data["cost_gemini"]),

    ImageModels.STABLE_DIFFUSION: Model(name="Stable Diffusion", cost=settings_data["cost_sd"]),
    ImageModels.MIDJOURNEY: Model(name="Midjourney", cost=settings_data["cost_midjourney"]),
    ImageModels.DALLE_2: Model(name="Dall-E 2", cost=settings_data["cost_dalle_2"]),
    ImageModels.DALLE_3: Model(name="Dall-E 3", cost=settings_data["cost_dalle_3"]),
    ImageModels.KANDINSKY: Model(name="Kandinsky", cost=settings_data["cost_kandinsky"]),

    VideoModels.TEXT_TO_VIDEO: Model(name="Текст в видео", cost=settings_data["cost_text_to_video"]),
    VideoModels.IMG_TO_VIDEO: Model(name="Фото в видео", cost=settings_data["cost_img_to_video"]),
    VideoModels.RMBG_VIDEO: Model(name="Удалить фон на видео", cost=settings_data["cost_rembg_video"]),
    VideoModels.CARTOON_VIDEO: Model(name="Видео в мультик", cost=settings_data["cost_cartoon_video"]),

    ServiceModels.DIPLOMA: Model(name="Учебные работы", cost=settings_data["cost_diploma"]),
}


class Settings(BaseSettings):
    DEBUG: bool = env.bool("DEBUG")
    SECRET_KEY: str = env.str("SECRET_KEY")

    BASE_DIR: Path = _base_dir
    MEDIA_DIR: Path = BASE_DIR / "tgbot_app" / "media"

    APP_NAME: str = settings_data["app_name"]
    DOMAIN: str = settings_data["domain"]

    TG_TOKEN: str = settings_data["tgbot_token"]
    BOT_USERNAME: str = settings_data["bot_username"]
    SUPPORT_USERNAME: str = settings_data["support_username"]
    TARGET_CHAT: str | None = settings_data["target_chat"]

    NEIRO_TOKEN: str = settings_data["api_token"]
    RAPIDAPI_TOKEN: str = settings_data["rapidapi_token"]

    PROXY_URL: str = settings_data["proxy_url"]

    ROBOKASSA_LOGIN: str = settings_data["robokassa_login"]
    ROBOKASSA_PASS1: str = settings_data["robokassa_pass1"]
    ROBOKASSA_PASS2: str = settings_data["robokassa_pass2"]

    DB_URL: str = f"postgresql+psycopg2://{_db_user}:{_db_pass}@{_db_host}:{_db_port}/{_db_name}"
    ASYNC_DB_URL: str = f"postgresql+asyncpg://{_db_user}:{_db_pass}@{_db_host}:{_db_port}/{_db_name}"
    REDIS_URL: str = env.str("REDIS_URL")

    FREE_GPT_QUERIES: int = settings_data["free_gpt_queries"]
    FREE_SD_QUERIES: int = settings_data["free_sd_queries"]
    FREE_DALLE2_QUERIES: int = settings_data["free_dalle2_queries"]

    MODELS: dict[str, Model] = models_data


settings = Settings()
