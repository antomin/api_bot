from typing import Any

from loguru import logger

from common.models import db, User, ReferalLink
from common.settings import settings


async def get_or_create_user(tgid: int, username: str, first_name: str, last_name: str, link_id: int | None) -> User:
    async with db.async_session_factory() as session:
        user: User = await session.get(User, tgid)
        link: ReferalLink = session.get(ReferalLink, link_id) if link_id else None

        if not user:
            user = User(id=tgid, username=username if username else str(tgid), first_name=first_name,
                        last_name=last_name, referal_link_id=link_id)
            user.chatgpt_daily_limit = settings.FREE_GPT_QUERIES
            user.sd_daily_limit = settings.FREE_SD_QUERIES
            user.dalle_2_daily_limit = settings.FREE_DALLE2_QUERIES

            session.add(user)

            if link_id:
                link.new_users += 1
                link.clicks += 1

            logger.info(f"New user <{tgid}>")

        else:
            if link and user.referal_link_id != link_id:
                link.clicks += 1

        await session.commit()

        return user


async def get_obj_by_id(obj: Any, id_: int | str) -> Any:
    async with db.async_session_factory() as session:
        result = await session.get(obj, id_)
        return result
