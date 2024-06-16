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
    desc: str


def get_settings():
    dict_data = {}
    with open(f"{_base_dir}/common/settings.json", "r", encoding="utf-8") as file:
        settings_raw_data = json.loads(file.read())

    for section, data in settings_raw_data.items():
        for key, info in data.items():
            dict_data[key] = info['value']

    return dict_data


settings_data = get_settings()

models_data = {
    TextModels.GPT_3_TURBO: Model(name="ChatGPT 3.5 Turbo", cost=int(settings_data["cost_gpt_3"]),
                                  desc="Это мощная модель от OpenAI с хорошей скоростью и качеством генерации. "
                                       "Нейросеть решает все текстовые задачи на достойном уровне"),
    TextModels.GPT_4_TURBO: Model(name="ChatGPT 4 Turbo", cost=int(settings_data["cost_gpt_4"]),
                                  desc="Это самая мощная версия GPT с невероятно высокой производительностью и лучшей "
                                       "точностью ответов. Статьи, копирайтинг, код, продающие слоганы – ChatGPT 4 "
                                       "Turbo выдает превосходный результат в очень широком спектре задач."),
    TextModels.YAGPT: Model(name="Яндекс GPT", cost=int(settings_data["cost_yagpt"]),
                            desc="Это российская версия модели GPT с акцентом на русский язык и адаптацию под "
                                 "специфику региона. Модель слегка уступает аналогам в креативности, но при этом "
                                 "крайне точна и быстра в генерации текста, кода и переводе."),
    TextModels.YAGPT_LITE: Model(name="Яндекс GPT Lite", cost=int(settings_data["cost_yagpt_lite"]),
                                 desc="Это легковесная версия модели Яндекс GPT. По качеству немного уступает своему "
                                      "старшему предшественнику, но может похвастаться скоростью и дешевой ценой "
                                      "запроса."),
    TextModels.CLAUDE: Model(name="Claude", cost=int(settings_data["cost_claude"]),
                             desc="Это модель, обладающая способностью к творчеству. Хорошо работает с текстом и "
                                  "общается более человечно, т.к. обучалась на данных реальных пользователей. Можно "
                                  "использовать, чтобы вести деловую переписку."),
    TextModels.GEMINI: Model(name="Gemini", cost=int(settings_data["cost_gemini"]),
                             desc="Это слегка упрощенный аналог ChatGPT от Google. Модель хороша в рутинных задачах. "
                                  "Владельцы онлайн-магазинов заполняют ей содержания карточек товаров."),

    ImageModels.MIDJOURNEY: Model(name="Midjourney", cost=int(settings_data["cost_midjourney"]),
                                  desc="Это самая крутая нейросеть для генерации картинок. Именно этой моделью "
                                       "создавались наиболее вирусные и запоминающиеся ИИ-картинки в интернете."),
    ImageModels.DALLE_3: Model(name="Dall-E 3", cost=int(settings_data["cost_dalle_3"]),
                               desc="Эта нейросеть входит в топ-3 самых мощных в мире. Она слегка уступает Midjourney "
                                    "в качестве генераций, но при этом лучше понимает человеческие запросы."),
    ImageModels.KANDINSKY: Model(name="Kandinsky", cost=int(settings_data["cost_kandinsky"]),
                                 desc="Это отечественная нейронка, которая лучше всех понимает запросы на русском. "
                                      "Модели достаточно написать буквально пару слов, остальное она додумает сама и "
                                      "выдаст потрясное, детализированное изображение."),

    VideoModels.TEXT_TO_VIDEO: Model(name="Текст в видео", cost=int(settings_data["cost_text_to_video"]), desc=""),
    VideoModels.IMG_TO_VIDEO: Model(name="Фото в видео", cost=int(settings_data["cost_img_to_video"]), desc=""),
    VideoModels.RMBG_VIDEO: Model(name="Удалить фон на видео", cost=int(settings_data["cost_rembg_video"]), desc=""),
    VideoModels.CARTOON_VIDEO: Model(name="Видео в мультик", cost=int(settings_data["cost_cartoon_video"]), desc=""),

    ServiceModels.DIPLOMA: Model(name="Учебные работы", cost=int(settings_data["cost_diploma"]), desc=""),
    ServiceModels.REWRITE: Model(name="Рерайт", cost=int(settings_data["cost_rewrite"]), desc=""),
    ServiceModels.VISION: Model(name="Решение по фото", cost=int(settings_data["cost_vision"]), desc=""),
    ServiceModels.ARTICLE: Model(name="Статьи", cost=int(settings_data["cost_article"]), desc=""),
    ServiceModels.STT: Model(name="STT", cost=int(settings_data["cost_stt"]), desc=""),
    ServiceModels.TTS: Model(name="TTS", cost=int(settings_data["cost_stt"]), desc=""),
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
    TARGET_CHAT: str = settings_data["target_chat"]
    TARGET_CHAT_LINK: str = settings_data["target_chat_link"]

    NEIRO_TOKEN: str = settings_data["api_token"]

    ROBOKASSA_LOGIN: str = settings_data["robokassa_login"]
    ROBOKASSA_PASS1: str = settings_data["robokassa_pass1"]
    ROBOKASSA_PASS2: str = settings_data["robokassa_pass2"]

    STARS_TOKEN: str = env.str("STARS_TOKEN")

    DB_URL: str = f"postgresql+psycopg2://{_db_user}:{_db_pass}@{_db_host}:{_db_port}/{_db_name}"
    ASYNC_DB_URL: str = f"postgresql+asyncpg://{_db_user}:{_db_pass}@{_db_host}:{_db_port}/{_db_name}"

    FREE_GEMINI_QUERIES: int = int(settings_data["free_gemini_queries"])
    FREE_SD_QUERIES: int = int(settings_data["free_sd_queries"])
    FREE_KANDINSKY_QUERIES: int = int(settings_data["free_kandinsky_queries"])

    MODELS: dict[str, Model] = models_data


settings = Settings()
