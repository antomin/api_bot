from .neiro_api import Midjourney, OpenAI, StableDiffusion, Yandex, Gemini, Claude
from common.settings import settings

midjourney = Midjourney(token=settings.NEIRO_TOKEN)
openai = OpenAI(token=settings.NEIRO_TOKEN)
sd = StableDiffusion(token=settings.NEIRO_TOKEN)
yandex = Yandex(token=settings.NEIRO_TOKEN)
gemini = Gemini(token=settings.NEIRO_TOKEN)
claude = Claude(token=settings.NEIRO_TOKEN)
