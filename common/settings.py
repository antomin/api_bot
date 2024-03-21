from environs import Env
from pydantic_settings import BaseSettings

env = Env()
env.read_env("../.env")

_db_host: str = env.str("DB_HOST")
_db_port: int = env.int("DB_PORT")
_db_name: str = env.str("DB_NAME")
_db_user: str = env.str("DB_USER")
_db_pass: str = env.str("DB_PASS")


class Settings(BaseSettings):
    DEBUG: bool = env.bool("DEBUG")
    SECRET_KEY: str = env.str("SECRET_KEY")

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


settings = Settings()
