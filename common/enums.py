from enum import Enum


class TextModels(str, Enum):
    GPT_3_TURBO = "gpt-3.5-turbo-1106"
    GPT_4_TURBO = "gpt-4-1106-preview"
    CLAUDE = "claude"
    GEMINI = "gemini"
    YAGPT = "yandexgpt"
    YAGPT_LITE = "yandexgpt_lite"


class ImageModels(str, Enum):
    MIDJOURNEY = "midjourney"
    STABLE_DIFFUSION = "sd"
    DALLE_2 = "dall-e-2"
    DALLE_3 = "dall-e-3"
    KANDINSKY = "kandinsky"


class VideoTypes(str, Enum):
    PICA = "pica"
    TEXT_TO_VIDEO = "txt2mpeg"
    IMG_TO_VIDEO = "img2mpg"
    RMBG_VIDEO = "rembg"
    CARTOON_VIDEO = "cart2mpeg"
