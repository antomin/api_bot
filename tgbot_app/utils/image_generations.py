import asyncio
import uuid

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from common.db_api import create_image_query, update_object
from common.enums import ImageAction, ImageModels
from common.models import ImageQuery
from tgbot_app.services import neiro_api
from tgbot_app.services.neiro_api import GenerationStatus
from tgbot_app.utils.enums import GenerationResult


async def wait_image_result(model: ImageModels, task_id: str, status: Message, img_query: ImageQuery
                            ) -> GenerationResult:
    for _ in range(60):
        await asyncio.sleep(10)

        result = await neiro_api.get_image_status(task_id=task_id, model=model)

        if not result.success:
            continue

        if result.status in (GenerationStatus.ERROR, GenerationStatus.BANNED):
            await update_object(img_query, status=result.status)
            return GenerationResult(success=False, status=result.status)

        if result.status == GenerationStatus.WAITING:
            try:
                await status.edit_text("🕗 В ожидании начала генерации... Это может занять 3-5 минут...")
            except TelegramBadRequest:
                pass
            continue

        if result.status == GenerationStatus.IN_PROCESS:
            try:
                await status.edit_text(f"🖌️ Рисуем Ваше изображение... {result.result}")
            except TelegramBadRequest:
                pass
            continue

        if result.status == GenerationStatus.READY:
            result = result.result if model == ImageModels.MIDJOURNEY else result.result[0]
            await update_object(img_query, status=GenerationStatus.READY, result=result)
            return GenerationResult(result=result, task_id=img_query.id)

    await update_object(img_query, status=GenerationStatus.ERROR, result='timeout')
    return GenerationResult(success=False)


async def run_mj_generation(action: ImageAction, status: Message, task_id: str = "", prompt: str = "",
                            index: int | None = None) -> GenerationResult:
    if action == ImageAction.IMAGINE:
        result = await neiro_api.imagine(model=ImageModels.MIDJOURNEY, prompt=prompt)
    else:
        result = await neiro_api.midjourney_action(action=action, index=index, task_id=task_id)

    if not result.success:
        return result

    cur_task_id = result.result

    img_query = await create_image_query(id=cur_task_id, user_id=status.chat.id, model=ImageModels.MIDJOURNEY,
                                         action=action, index=index, prompt=prompt)

    return await wait_image_result(model=ImageModels.MIDJOURNEY, task_id=cur_task_id, status=status,
                                   img_query=img_query)


async def run_image_generation(model: ImageModels, prompt: str, status: Message) -> GenerationResult:
    result = await neiro_api.imagine(model=model, prompt=prompt)

    if not result.success:
        return result

    await status.edit_text("🖌️ Рисуем Ваше изображение...")

    task_id = result.result

    img_query = await create_image_query(id=task_id, user_id=status.chat.id, model=model, action=ImageAction.IMAGINE,
                                         prompt=prompt)

    return await wait_image_result(model=model, task_id=task_id, status=status, img_query=img_query)
