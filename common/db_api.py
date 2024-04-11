from typing import Any

from loguru import logger
from sqlalchemy import select

from common.enums import TextModels
from common.models import ReferalLink, TextGenerationRole, User, db
from common.models.generations import ImageQuery, TextQuery, TextSession
from common.settings import Model, settings


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
            text_session = TextSession(user_id=user.id)
            user.text_session = text_session

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


async def update_object(obj: Any, update_relations: bool = False, **params) -> None:
    async with db.async_session_factory() as session:
        for field, value in params.items():
            setattr(obj, field, value)
        session.add(obj)
        await session.commit()

        if update_relations:
            await session.refresh(obj)


async def get_roles() -> list[TextGenerationRole]:
    async with db.async_session_factory() as session:
        result = await session.scalars(
            select(TextGenerationRole).where(TextGenerationRole.is_active).order_by(TextGenerationRole.id)
        )

        return result.all()


async def switch_context(user: User) -> None:
    async with db.async_session_factory() as session:
        if not user.text_session_id:
            user.text_session = TextSession()
        else:
            await session.delete(user.text_session)
            user.text_session_id = None

        session.add(user)
        await session.commit()
        await session.refresh(user)


async def reset_session(user: User) -> None:
    if not user.text_session_id:
        return

    async with db.async_session_factory() as session:
        old_session = user.text_session
        user.text_session = TextSession(user=user)
        await session.delete(old_session)
        session.add(user)
        await session.commit()
        await session.refresh(user)


async def get_messages(session_id: int) -> list[TextQuery]:
    async with db.async_session_factory() as session:
        messages = await session.scalars(select(TextQuery).where(TextQuery.session_id == session_id))
        return messages.all()


async def create_text_query(user_id: int, session_id: int, prompt: str, result: str, model: TextModels) -> None:
    async with db.async_session_factory() as session:
        session.add(
            TextQuery(model=model, session_id=session_id, user_id=user_id, prompt=prompt, result=result)
        )
        await session.commit()


async def change_balance(user: User, model: Model, add: bool = False) -> None:  # TODO Review
    cost = model.cost if add else -model.cost

    if user.tariff:
        if model.name == "ChatGPT 3.5 Turbo":
            return
        user.token_balance += cost
    else:
        if model.name == "ChatGPT 3.5 Turbo" and (user.chatgpt_daily_limit > 0 or (add and user.token_balance < model.cost)):
            user.chatgpt_daily_limit += 1 if add else -1
        elif model.name == "Dall-E 2" and (user.dalle_2_daily_limit > 0 or (add and user.token_balance < model.cost)):
            user.dalle_2_daily_limit += 1 if add else -1
        elif model.name == "Stable Diffusion" and (user.sd_daily_limit > 0 or (add and user.token_balance < model.cost)):
            user.sd_daily_limit += 1 if add else -1
        else:
            user.token_balance += cost

    async with db.async_session_factory() as session:
        session.add(user)
        await session.commit()


async def create_image_query(**params) -> ImageQuery:
    query = ImageQuery(**params)
    async with db.async_session_factory() as session:
        session.add(query)
        await session.commit()

    return query

