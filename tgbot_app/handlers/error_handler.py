from aiogram import Router
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, Message

router = Router()


@router.errors()
@router.error()
async def handle_cancel_exception(event: ErrorEvent):
    if isinstance(event.exception, CancelHandler):
        pass
