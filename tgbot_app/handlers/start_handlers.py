from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from common.models import User
from common.settings import settings
from tgbot_app.keyboards import main_kb

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext, user: User):
    await state.clear()

    text = (f"🤖 <b>Привет, я бот {settings.APP_NAME}</b>\n"
            f"Вы можете использовать любые нейросети или сервисы, генерировать текст, картинки, видео, человеческую "
            f"речь или пользоваться сервисами для генерации полноценных работ и обработки файлов.\n\n"
            f"💎 <b>Как работают токены?</b>\nКаждый запрос в нейросеть или сервис стоит определенное кол-во токенов. "
            f"Токены это виртуальная валюта, их Вы можете купить или получить ежемесячно по подписки.\n\n"
            f"<b>Советы к правильному использованию:</b>\n"
            f"– Задавайте осмысленные вопросы, расписывайте детальнее.\n"
            f"– Не пишите ерунду, иначе получите её же в ответ.\n"
            f"– Погуглите промпты для генерации, чтобы не тратить токены на самостоятельные попытки.\n\n"
            f"<i>* — при нажатии на кнопку или команду, Вы разрешаете боту присылать Вам сообщения и рассылки. "
            f"У премиум пользователей рекламы нет.</i>")
    markup = await main_kb()

    await message.answer(text=text, reply_markup=markup)
