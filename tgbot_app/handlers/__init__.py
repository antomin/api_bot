from aiogram import Router

from .start_handlers import router as start_router
from .ais_handler import router as ais_router
from .faq_handler import router as faq_router
from .profile_handler import router as profile_router
from .services_handler import router as services_router
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
)
