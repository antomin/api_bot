import asyncio
import json
import time
from datetime import datetime

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError, TelegramRetryAfter
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from loguru import logger
from sqlalchemy import update, select

from common.models import ReferalLink, User, db
from common.settings import settings
from tgbot_app.keyboards import main_kb

TARIFFS = {
    50.0: 2,
    150.0: 3,
    500.0: 4,
}

errors = []


def get_data(path: str) -> list:
    with open(path, 'r') as file:
        data = file.read()

    return json.loads(data)


def parse_name(name: str) -> list:
    _names = name.split(" ")
    if len(_names) == 2:
        return _names
    else:
        if _names[0] == "need_update":
            return [None, None]
        return [_names[0], None]


def str_to_datetime(date_str: str) -> datetime:
    date_str = date_str.split(".")[0]
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    return dt


def calc_update_time(date_str: str) -> datetime:
    dt = str_to_datetime(date_str)
    now = datetime.now()
    result = datetime(year=now.year, month=now.month, day=now.day, hour=dt.hour, minute=dt.minute, second=dt.second)
    return result


def calc_payment_time(user: dict, invoices: list[dict]) -> (datetime | None, int | None):
    if user["type"] != "subscription":
        return None, None
    user_invoices_to_paid = [inv for inv in invoices if inv['payment_status'] == 'due-on-date' and user["id"] == inv["user_id"]]
    if not user_invoices_to_paid:
        return None, None
    last_inv = user_invoices_to_paid[-1]
    dt = str_to_datetime(last_inv['next_payment_date'])

    if dt < datetime(year=2024, month=5, day=14):
        return None, None

    return dt, last_inv['parent_invoice_id']


def calc_tariff(type_: str, quantity: float) -> dict:
    if type_ == "subscription":
        return {
            "tariff_id": TARIFFS.get(quantity),
            "chatgpt_daily_limit": -1,
            "gemini_daily_limit": -1,
            "kandinsky_daily_limit": 5,
            "sd_daily_limit": -1,
        }
    else:
        return {
            "tariff_id": None,
            "chatgpt_daily_limit": 0,
            "gemini_daily_limit": 5,
            "kandinsky_daily_limit": 2,
            "sd_daily_limit": 0,
        }


def get_mother_inv_id(user_id: int, invoices: list[dict]) -> int | None:
    user_invoices = [inv["parent_invoice_id"] for inv in invoices if inv["user_id"] == user_id and inv["parent_invoice_id"]]
    if user_invoices:
        return max(user_invoices)


def create_users(users: list[dict], invoices: list[dict]) -> None:
    logger.info("Creating users")
    cnt = len(users)

    for user in users:
        names = parse_name(user["full_name"])
        # mother_invoice_id = get_mother_inv_id(user["id"], invoices)

        payment_time, mother_invoice_id = calc_payment_time(user, invoices)

        if user["type"] == "subscription" and payment_time and mother_invoice_id:
            tariff_id = TARIFFS.get(user["quantity"])
            chatgpt_daily_limit = -1
            gemini_daily_limit = -1
            kandinsky_daily_limit = 5
            sd_daily_limit = -1
            first_payment = False
        else:
            tariff_id = None
            chatgpt_daily_limit = 0
            gemini_daily_limit = 5
            kandinsky_daily_limit = 2
            sd_daily_limit = 0
            first_payment = True
            payment_time = None
            mother_invoice_id = None

        user_obj = User(
            id=user["user_id"],
            username=user["username"],
            first_name=names[0],
            last_name=names[1],
            is_active=True if user["active"] in (1, None) else False,
            chatgpt_daily_limit=chatgpt_daily_limit,
            gemini_daily_limit=gemini_daily_limit,
            kandinsky_daily_limit=kandinsky_daily_limit,
            sd_daily_limit=sd_daily_limit,
            token_balance=int(user["left"]) * 15 if user["left"] else 0,
            update_daily_limits_time=calc_update_time(user["created_at"]) if user["created_at"] else datetime.now(),
            tariff_id=tariff_id,
            mother_invoice_id=mother_invoice_id,
            payment_time=payment_time,
            first_payment=first_payment,
            created_at=str_to_datetime(user["created_at"]) if user["created_at"] else datetime.now(),
        )

        try:
            with db.session_factory() as session:
                session.add(user_obj)
                session.commit()
        except Exception as error:
            logger.error(f"Creating user <{user['user_id']}> failed: {error.args}")
            errors.append({"user_id": user["user_id"], "error": error.args})

        cnt -= 1
        print(f"USERS: {cnt}")

    logger.info("Creating users FINISH")


def create_links(links: list[dict], users: list[dict], invoices: list[dict]) -> None:
    logger.info("Creating links")
    default_owner_id = 5367092501
    cnt = len(links)

    for link in links:
        link_obj = ReferalLink(
            id=link["id"],
            name=link["name"],
            owner_id=default_owner_id,
            site_link=f"https://chatgpt-neyroset.ru/redirect/{link['id']}/",
            bot_link=f"https://t.me/chatgpt_gpt4bot?start={link['id']}",
            created_at=str_to_datetime(link["created_at"]),
        )

        users_ids = [user["user_id"] for user in users if user["link_id"] == link["id"] and user["full_name"] != "need_update"]
        invoices_amounts = [int(inv["amount"]) for inv in invoices if inv['payment_status'] == "success" and inv["user_id"] in users_ids]
        users_cnt = len(users_ids)

        link_obj.new_users = users_cnt
        link_obj.clicks = users_cnt
        link_obj.buys_cnt = len(invoices_amounts)
        link_obj.buys_sum = sum(invoices_amounts)

        try:
            with db.session_factory() as session:
                for user_id in set(users_ids):
                    user = session.get(User, user_id)
                    link_obj.users.append(user)

                    session.add(user)

                    users_cnt -= 1
                    print(f"LINK {link['id']} Users: {users_cnt}")

                session.add(link_obj)
                session.commit()

        except Exception as error:
            logger.error(f"Creating link <{link['id']}> failed: {error.args}")
            errors.append({"link_id": link["id"], "error": error.args})

        cnt -= 1
        print(f"LINKS: {cnt}")

    logger.info("Creating links FINISH")


def delete_data() -> None:
    logger.info("Deleting data")
    with db.session_factory() as session:
        # session.query(User).delete()
        session.query(ReferalLink).delete()
        session.commit()

    logger.info("Deleting data FINISH")


def main():
    users = get_data("fixtures/json_users.json")
    invoices = get_data("fixtures/json_invoices.json")
    links = get_data("fixtures/json_links.json")

    # create_users(users, invoices)
    create_links(links, users, invoices)


def save_errors():
    with open("errors.log", "w") as file:
        file.write("\n".join(str(e) for e in errors))


def switch_model():
    with db.session_factory() as session:
        stmt = update(User).where(User.txt_model != "gemini-pro").values(txt_model="txt_model")
        session.execute(stmt)
        session.commit()


def create_users_files():
    with db.session_factory() as session:
        free_users = session.scalars(select(User.id).where(User.tariff_id.is_(None), User.is_active)).all()
        prem_users = session.scalars(select(User.id).where(User.tariff_id.is_not(None), User.is_active)).all()

        with open("free_users.txt", "w") as file:
            file.write("\n".join(map(str, free_users)))

        with open("prem_users.txt", "w") as file:
            file.write("\n".join(map(str, prem_users)))


async def update_keyboard_process(user_id: int, bot: Bot, semaphore, markup: ReplyKeyboardMarkup) -> None:
    async with semaphore:
        start = time.time()
        try:
            await bot.send_message(chat_id=user_id, reply_markup=markup, disable_notification=True, text=".")
            logger.info(f"User <{user_id}> sent keyboard markup>")
        except (TelegramBadRequest, TelegramForbiddenError):
            async with db.async_session_factory() as session:
                await session.execute(update(User).where(User.id == user_id).values(is_active=False))
                logger.info(f"User <{user_id}> inactive")
        except TelegramRetryAfter as error:
            await asyncio.sleep(error.retry_after)
            await update_keyboard_process(user_id, bot, semaphore, markup)
        except Exception as error:
            logger.error(f"Update keyboard process failed: {error.args}")
        finally:
            work_time = time.time() - start
            if work_time < 1:
                await asyncio.sleep(1 - work_time)


async def update_keyboard():
    async with db.async_session_factory() as session:
        result = await session.scalars(select(User.id).where(User.is_active))
        users = result.all()

    bot = Bot(token=settings.BOT_TOKEN)
    semaphore = asyncio.Semaphore(value=25)
    markup = await main_kb()
    tasks = []

    for user in users:
        tasks.append(asyncio.create_task(update_keyboard_process(user, bot, semaphore, markup)))


if __name__ == '__main__':
    # delete_data()
    # main()
    # save_errors()
    # switch_model()
    # create_users_files()
    asyncio.run(update_keyboard())
