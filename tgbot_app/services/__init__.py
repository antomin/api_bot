from common.settings import settings

from .neiro_api import AsyncNeiroAPI, Yandex
from .translator import Translator

neiro_api = AsyncNeiroAPI(token=settings.NEIRO_TOKEN)
translator = Translator(token=settings.RAPIDAPI_TOKEN, proxy_url=settings.PROXY_URL)
yandex = Yandex(token=settings.NEIRO_TOKEN)
