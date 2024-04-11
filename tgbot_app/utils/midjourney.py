import asyncio

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from common.db_api import create_image_query, update_object
from common.enums import ImageAction, ImageModels
from tgbot_app.services import neiro_api
from tgbot_app.services.neiro_api import GenerationStatus
from tgbot_app.utils.enums import GenerationResult


async def run_mj_generation(action: ImageAction, status: Message, task_id: str = "", prompt: str = "",
                            index: int | None = None) -> GenerationResult:
    if action == ImageAction.IMAGINE:
        result = await neiro_api.midjourney_imagine(prompt)
    else:
        result = await neiro_api.midjourney_action(action=action, index=index, task_id=task_id)

    if not result.success:
        return result

    cur_task_id = result.result

    img_query = await create_image_query(id=cur_task_id, user_id=status.chat.id, model=ImageModels.MIDJOURNEY,
                                         action=action, index=index, prompt=prompt)

    for _ in range(60):
        await asyncio.sleep(10)

        wait_result = await neiro_api.midjourney_status(task_id=cur_task_id)

        if not wait_result.success:
            continue

        if wait_result.status == GenerationStatus.ERROR:
            await update_object(img_query, status=GenerationStatus.ERROR)
            return GenerationResult(success=False)

        if wait_result.status == GenerationStatus.BANNED:
            await update_object(img_query, status=GenerationStatus.BANNED)
            return GenerationResult(success=False, status=GenerationStatus.BANNED)

        if wait_result.status == GenerationStatus.WAITING:
            try:
                await status.edit_text("🕗 В ожидании начала генерации... Это может занять 3-5 минут...")
            except TelegramBadRequest:
                pass

            continue

        if wait_result.status == GenerationStatus.IN_PROCESS:
            try:
                await status.edit_text(f'🖌️ Рисуем Ваше изображение... {wait_result.result}')
            except TelegramBadRequest:
                pass

            continue

        if wait_result.status == GenerationStatus.READY:
            await update_object(img_query, status=GenerationStatus.READY)
            return GenerationResult(result=wait_result.result, task_id=img_query.id)

    await update_object(img_query, status=GenerationStatus.ERROR, result='timeout')
    return GenerationResult(success=False)
