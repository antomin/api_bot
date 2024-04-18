from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from common.settings import settings

from tgbot_app.keyboards import (gen_back_faq_kb, gen_faq_finances_kb,
                                 gen_faq_finances_sub_kb, gen_faq_inline_kb,
                                 gen_faq_problems_kb, gen_faq_rec_kb,
                                 gen_main_faq_kb)
from tgbot_app.utils.callbacks import FAQCallback
from tgbot_app.utils.enums import (FAQFinancesButtons, FAQMainButtons,
                                   FAQProblemsButtons, FAQRecButtons,
                                   MainButtons, DefaultCommands)

router = Router()


@router.callback_query(FAQCallback.filter(F.chapter == MainButtons.FAQ))
@router.message(F.text == MainButtons.FAQ.value)
@router.message(Command(DefaultCommands.faq.name))
async def start_faq(message: Message | CallbackQuery, state: FSMContext):
    await state.clear()

    if isinstance(message, CallbackQuery):
        await message.answer()
        message = message.message

    await message.answer(text="❓<b>Часто задаваемые вопросы:</b>", reply_markup=await gen_main_faq_kb())


@router.callback_query(FAQCallback.filter(F.chapter == FAQMainButtons.PREMIUM))
async def faq_premium(callback: CallbackQuery):
    await callback.answer()

    text = ("💳Подписка предоставляем Вам ежемесячно определенное кол-во токенов, в зависимости от выбранного тарифа. "
            "Если у Вас оформлена подписка, то  стоимость токенов для Вас в 2 раза дешевле обычной. Подписка "
            "продлевается автоматически каждые 30 дней. Автоматическое продление Вы можете отключить в разделе "
            "подписка.")
    markup = await gen_back_faq_kb(to_chapter=MainButtons.FAQ)

    await callback.message.answer(text=text, reply_markup=markup)


@router.callback_query(FAQCallback.filter(F.chapter == FAQMainButtons.TOKENS))
async def faq_tokens(callback: CallbackQuery):
    await callback.answer()

    text = ("💎 Токены это виртуальная валюта с помощью которой Вы можете оплачивать Ваши генерации в нейросетях и "
            "сервисах. Стоимость генерации в нейросети или сервисе на прямую зависит от реальной стоимости у "
            "создателя. Мы являемся агрегатором и предоставляем Вам доступ к нейросетям.\n\n"
            "* По подписки стоимость токенов в 2 раза дешевле.")
    markup = await gen_back_faq_kb(to_chapter=MainButtons.FAQ)

    await callback.message.answer(text=text, reply_markup=markup)


@router.callback_query(FAQCallback.filter(F.chapter == FAQMainButtons.RECOMMENDATIONS))
async def faq_recommendations(callback: CallbackQuery, callback_data: FAQCallback):
    await callback.answer()

    sub_chapter = callback_data.sub_chapter

    markup = await gen_back_faq_kb(to_chapter=FAQMainButtons.RECOMMENDATIONS)

    if sub_chapter == FAQRecButtons.USE.name:
        text = ("🔹 Телеграм  бот предоставляет доступ к нейросетям для генерации текст, изображений, и даже "
                "человеческой речи. Кроме этого мы создали несколько сервисов упрощающих работу для разных областей, "
                "которые помогут в решении разных вопросов. Например генерации полноценны учебных работ, генерации seo "
                "статей, рерайтинг, текст в речь и речь в текст. Используйте свои запросы  к  нейросети с умом для "
                "решения Ваших повседневных задач.")

    elif sub_chapter == FAQRecButtons.AIS.name:
        text = ("🔹 Чтобы получить нужный результат от работы нейросети, нужно научиться правильно составлять запросы. "
                "Перед началом работы с нейросетям ознакомиться с тем, как правильно делать запросы к той или другой "
                "нейросети. Мы не проводим обучения по использованию нейросетями, наша задача - это предоставить Вам "
                "удобный доступ к ним в одном месте.")

    elif sub_chapter == FAQRecButtons.WORK.name:
        text = ("🔹 Мы создали  сервис для полноценной генерации учебных работ: дипломов, курсовых, эссе, рефератов. "
                "По окончании генерации Вы получаете полноценный word файл, в среднем, на 40-50 страниц. Существует "
                "два режима: автоматический и ручной. Автоматический режим это когда нейросеть сама придумает за Вас "
                "список тем и подглав, а в ручном режиме Вы сможете самостоятельно задать темы и подглавы, следуя "
                "инструкциям.")

    else:
        text = "🔹Краткие рекомендации для новичков, как можно использовать наш телеграмм бот."
        markup = await gen_faq_rec_kb()

    await callback.message.answer(text=text, reply_markup=markup)


@router.callback_query(FAQCallback.filter(F.chapter == FAQMainButtons.PROBLEMS))
async def faq_problems(callback: CallbackQuery, callback_data: FAQCallback):
    await callback.answer()

    sub_chapter = callback_data.sub_chapter

    markup = await gen_back_faq_kb(to_chapter=FAQMainButtons.PROBLEMS)

    if sub_chapter == FAQProblemsButtons.AI.name:
        text = ("🔹 Нейросети могут не работать по разным причинам. Если что-то не работает, нам отправляется "
                "уведомление о проблеме, и мы обязательно ее устраним в кратчайшие сроки. Однако, часто бывает, что "
                "нейросети ломаются на стороне их создателя. В этом случае мы просто ждем когда все заработает "
                "вместе с Вами.")

    elif sub_chapter == FAQProblemsButtons.SERVICE.name:
        text = ("🔹 Сервисы могут не работать по разным причинам. Если что-то не работает, нам отправляется "
                "уведомление о проблеме, и мы обязательно ее устраним в кратчайшие сроки. Все сервисы основаны на "
                "нейросетях, и часто бывает, что нейросети ломаются на стороне их создателя. В этом случае мы просто "
                "ждем когда все заработает вместе с Вами")

    else:
        text = "🔹Выберите категорию вашей проблемы, чтобы мы смогли Вам помочь или нажмите кнопку перезапустить бота."
        markup = await gen_faq_problems_kb()

    await callback.message.answer(text=text, reply_markup=markup)


@router.callback_query(FAQCallback.filter(F.chapter == FAQMainButtons.INLINE))
async def faq_inline(callback: CallbackQuery, callback_data: FAQCallback):
    await callback.answer()

    sub_chapter = callback_data.sub_chapter

    if sub_chapter == "cmds":
        text = ("🔹У бота есть несколько команд:\n"
                "<code>/text</code> - по этой команде можно задать вопрос к ChatGPT 3.5 turbo\n"
                "<code>/img</code> - по этой команде можно задать запрос к нейросети StableDiffusion")
        markup = await gen_back_faq_kb(to_chapter=FAQMainButtons.INLINE)

    else:
        text = ("🔹Наш телеграмм бот можно добавить в Ваш чат телеграмм, и тогда все участники смогут им пользоваться, "
                "но лимиты у каждого участника будут индивидуальны.")
        markup = await gen_faq_inline_kb()

    await callback.message.answer(text=text, reply_markup=markup)


@router.callback_query(FAQCallback.filter(F.chapter == FAQMainButtons.FINANCES))
async def faq_finances(callback: CallbackQuery, callback_data: FAQCallback):
    await callback.answer()

    sub_chapter = callback_data.sub_chapter
    markup = await gen_back_faq_kb(to_chapter=FAQMainButtons.FINANCES)

    if sub_chapter in (FAQFinancesButtons.PREMIUM.name, FAQFinancesButtons.TOKENS.name):
        text = ("🔹Время работы оператора: с 10:00 до 20:00 с понедельника по пятницу. Пожалуйста, приготовьте чек, "
                "отправленный Вам на почту, которую Вы указывали при оплате. Нам нужен именно этот чек. Чек из "
                "приложения Вашего банка не подойдет. Так же приготовьте Ваш id. Его можно найти в разделе профиль. "
                "Как только Вы приготовите все необходимое, напишите оператору.")
        markup = await gen_faq_finances_sub_kb()

    elif sub_chapter == FAQFinancesButtons.RECURRING.name:
        text = ("🔹Продление выбранной подписки происходит автоматически, но ее можно отключить в разделе профиль. "
                "При этом Ваша текущая подписка сохранится, но средства за нее возвращены не будут. До конца срока "
                "вашей подписки Вы сможете покупать токены в 2 раза дешевле.")

    elif sub_chapter == FAQFinancesButtons.REFUND.name:
        text = (f"🔹При оформлении подписки Вы согласились с "
                f'<a href="{settings.DOMAIN}/offer/">публичным договором офертой</a>, а значит были ознакомлены с '
                f"порядком возврата средств. После оплаты подписки вам дается 48 часов на возврат, при условии что Вы "
                f"не потратили токены, которые Вам были начислены и не покупали новых токенов.\n\n"
                f"🔹Возврат средств можно запросить автоматически, для этого нужно:\n"
                f"Открыть бота >> Перейти в раздел подписка >> Отказаться от подписки >> далее следовать инструкции. "
                f"Если Вашему аккаунту уже недоступен возврат средств, Вы сможете отключить автопродление, а Ваша "
                f"текущая подписка сохранится.\n\n"
                f"🔹Время возврата средств зависит от Вашего банка. Обычно возврат средств занимает около 1 часа, но "
                f"иногда приходится ждать в течении недели, и в очень редких случаях месяц. После успешного создания "
                f"заявки на возврат средств Вам будет отправлено письмо на почту которую Вы указывали при покупки. "
                f"С этого момента узнать статус возврата средств Вы можете у платежного агрегатора Robokassa.")

    else:
        text = ("🔹У нас есть ответы на часто задаваемые вопросы касательно финансов. Ознакомьтесь с ними и следуйте "
                "рекомендациям чтобы решить Вашу проблему.")
        markup = await gen_faq_finances_kb()

    await callback.message.answer(text=text, reply_markup=markup, disable_web_page_preview=True)
