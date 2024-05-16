from aiogram import Router
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, Message

router = Router()


@router.error(ExceptionTypeFilter(CancelHandler))
async def handle_cancel_exception(event: ErrorEvent, message: Message):
    pass
