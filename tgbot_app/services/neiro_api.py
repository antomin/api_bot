from enum import Enum
from typing import Literal

from aiohttp import ClientSession
from loguru import logger
from pydantic import BaseModel

from common.enums import ImageAction, TextModels


class GenerationStatus(str, Enum):
    WAITING = "waiting"
    IN_QUEUE = "in_queue"
    IN_PROCESS = "in_process"
    READY = "ready"
    BANNED = "banned"
    ERROR = "error"


class ResponseResult(BaseModel):
    success: bool = True
    status: GenerationStatus | None = None
    result: str | None = None


class AsyncNeiroAPI:
    def __init__(self, token):
        self.headers = {"x-api-key": token}
        self.base_url = "https://api.mindl.in/v1"
        self.completion_urls = {
            TextModels.GPT_3_TURBO: f"{self.base_url}/openai/completion/",
            TextModels.GPT_4_TURBO: f"{self.base_url}/openai/completion/",
            TextModels.YAGPT: f"{self.base_url}/yandex/completion/",
            TextModels.YAGPT_LITE: f"{self.base_url}/yandex/completion/",
            TextModels.CLAUDE: f"{self.base_url}/claude/completion/",
            TextModels.GEMINI: f"{self.base_url}/gemini/completion/",
        }

    async def midjourney_imagine(self, prompt: str) -> ResponseResult:
        url = f"{self.base_url}/midjourney/imagine/"
        payload = {"prompt": prompt}

        result = await self.__request(url=url, payload=payload)

        if not result:
            return ResponseResult(success=False)
        return ResponseResult(result=result["task_id"])

    async def midjourney_action(self, action: ImageAction, index: int, task_id: str) -> ResponseResult:
        url = f"{self.base_url}/midjourney/action/"
        payload = {"action": action.value, "index": index, "task_id": task_id}

        result = await self.__request(url=url, payload=payload)

        if not result:
            return ResponseResult(success=False)
        return ResponseResult(result=result["task_id"])

    async def midjourney_status(self, task_id: str) -> ResponseResult:
        url = f"{self.base_url}/midjourney/check-task/"
        payload = {"task_id": task_id}

        result = await self.__request(url=url, payload=payload)

        if not result:
            return ResponseResult(success=False)
        return ResponseResult(status=result["status"], result=result["result"])

    async def completion(self, model: TextModels,
                         conversation: list[dict[Literal["role", "content"], str]]) -> ResponseResult:
        url = self.completion_urls[model]
        payload = {"model": model, "messages": conversation}

        result = await self.__request(url=url, payload=payload)

        if not result:
            return ResponseResult(success=False)
        return ResponseResult(result=result["result"])

    async def __request(self, url: str, payload: dict) -> dict:
        async with ClientSession(headers=self.headers) as session:
            async with session.post(url=url, json=payload) as response:
                if response.ok:
                    result = await response.json()
                    return result
                logger.error(f"API REQUEST error: {response.status} | {response.reason}")






#
#
#
#
#
# class Midjourney:
#     def __init__(self, token):
#         self.headers = {"x-api-key": token}
#         self.url = "https://api.нейросети.com/midjourney/"
#
#     async def imagine(self, prompt: str) -> GenerationResult:
#         return GenerationResult(result='uuuuuiiiiiddddd')
#
#     async def action(self, action: ImageAction, index: int, task_id: str) -> GenerationResult:
#         return GenerationResult(result=f"{action}|{index}|{task_id}")
#
#
# class TextGenerator:
#     def __init__(self, token):
#         self.headers = {"x-api-key": token}
#         self.url = "https://api.нейросети.com/midjourney/"
#
#     async def run_generation(self, model: TextModels, conversation: list[dict]) -> GenerationResult:
#         return GenerationResult(result=f"Model: {model} answer: {str(conversation)}")  # TODO
#
#
# class OpenAI:
#     def __init__(self, token):
#         self.headers = {"x-api-key": token}
#         self.url = "https://api.нейросети.com/openai/"
#
#
# class StableDiffusion:
#     def __init__(self, token):
#         self.headers = {"x-api-key": token}
#         self.url = "https://api.нейросети.com/stablediffusion/"
#
#     async def gen_image(self, prompt) -> GenerationResult:
#         return GenerationResult(result="https://w7.pngwing.com/pngs/895/199/png-transparent-spider-man-heroes-download-with-transparent-background-free-thumbnail.png")
#
#
#
# class Gemini:
#     def __init__(self, token):
#         self.headers = {"x-api-key": token}
#         self.url = "https://api.нейросети.com/bard/"
#
#
# class Claude:
#     def __init__(self, token):
#         self.headers = {"x-api-key": token}
#         self.url = "https://api.нейросети.com/claude/"
#
#
class Yandex:
    def __init__(self, token):
        self.headers = {"x-api-key": token}
        self.url = "https://api.нейросети.com/yandex/"

    async def speach_to_text(self) -> str:  # TODO
        return "Привет"
#
#
# class Translator:
#     def __init__(self, token):
#         self.headers = {"x-api-key": token}
#         self.url = "https://api.нейросети.com/translate/"
#
#     async def translate(self, text: str) -> GenerationResult:
#         return GenerationResult(result="Hello World!")
#
