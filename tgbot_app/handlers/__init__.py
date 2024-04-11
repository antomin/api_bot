from aiogram import Router

from .ais_handler import router as ais_router
from .faq_handler import router as faq_router
from .gen_image_handler import router as image_router
from .gen_text_handler import router as text_router
from .gen_video_handler import router as video_router
from .modes_handler import router as modes_router
from .profile_handler import router as profile_router
from .services_handler import router as services_router
from .start_handlers import router as start_router
from .subscription_handler import router as subscription_router
from .tokens_handler import router as tokens_router

main_router = Router()

main_router.include_routers(
    ais_router,
    faq_router,
    profile_router,
    services_router,
    start_router,
    subscription_router,
    tokens_router,
    modes_router,
    image_router,
    text_router,
    video_router
)
