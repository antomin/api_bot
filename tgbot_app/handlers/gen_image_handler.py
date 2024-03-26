from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from common.models import User
from tgbot_app.utils.states import GenerationState

router = Router()


@router.callback_query(GenerationState.IMAGE)
async def run_image_generation(message: Message, state: FSMContext, user: User):
    pass
