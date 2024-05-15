import json
from datetime import datetime
from pprint import pprint

from loguru import logger

from common.models import ReferalLink, User, db

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
    paid_user_invoices = set([inv["parent_invoice_id"] for inv in invoices if inv['payment_status'] == "success" and inv["user_id"] == user_id and inv["parent_invoice_id"] is not None])
    if paid_user_invoices:
        return max(paid_user_invoices)


def create_users(users: list[dict], invoices: list[dict]) -> None:
    logger.info("Creating users")
    cnt = len(users)

    with db.session_factory() as session:
        for user in users:
            if user["full_name"] == "need_update":
                continue

            try:
                names = parse_name(user["full_name"])
                tariff = calc_tariff(type_=user["type"], quantity=user["quantity"])

                user_obj = User(
                    id=user["user_id"],
                    username=user["username"],
                    first_name=names[0],
                    last_name=names[1],
                    is_active=True if user["active"] else False,
                    chatgpt_daily_limit=tariff["chatgpt_daily_limit"],
                    gemini_daily_limit=tariff["gemini_daily_limit"],
                    kandinsky_daily_limit=tariff["kandinsky_daily_limit"],
                    sd_daily_limit=tariff["sd_daily_limit"],
                    token_balance=int(user["left"]) * 6 if user["left"] else 0,
                    update_daily_limits_time=calc_update_time(user["created_at"]) if user["created_at"] else datetime.now(),
                    tariff_id=tariff["tariff_id"],
                    mother_invoice_id=get_mother_inv_id(user["id"], invoices),
                    payment_time=str_to_datetime(user["expiration_date"]) if tariff["tariff_id"] else None,
                    created_at=str_to_datetime(user["created_at"]) if user["created_at"] else datetime.now(),
                )

                session.add(user_obj)
                session.commit()
            except Exception as error:
                logger.error(f"Creating user <{user['user_id']}> failed: {error}")
                errors.append({"user_id": user["user_id"], "error": error})

            cnt -= 1
            print(f"USERS: {cnt}")

        # session.commit()

    logger.info("Creating users FINISH")


def create_links(links: list[dict], users: list[dict], invoices: list[dict]) -> None:
    logger.info("Creating links")
    default_owner_id = 5367092501
    cnt = len(links)

    with db.session_factory() as session:
        for link in links:
            try:
                link_obj = ReferalLink(
                    id=link["id"],
                    name=link["name"],
                    owner_id=default_owner_id,
                    site_link=f"https://chatgpt-neyroset.ru/redirect/{link['id']}/",
                    bot_link=f"https://t.me/chatgpt_gpt4bot?start={link['id']}",
                    created_at=str_to_datetime(link["created_at"]),
                )

                users_ids = [user["user_id"] for user in users if user["link_id"] == link["id"]]
                invoices_amounts = [int(inv["amount"]) for inv in invoices if inv['payment_status'] == "success" and inv["user_id"] in users_ids]
                users_cnt = len(users_ids)

                link_obj.new_users = users_cnt
                link_obj.clicks = users_cnt
                link_obj.buys_cnt = len(invoices_amounts)
                link_obj.buys_sum = sum(invoices_amounts)

                for user_id in users_ids:
                    user = session.get(User, user_id)
                    link_obj.users.append(user)

                    session.add(user)

                session.add(link)
                session.commit()

            except Exception as error:
                logger.error(f"Creating link <{link['id']}> failed: {error}")
                errors.append({"link_id": link["id"], "error": error})

            cnt -= 1
            print(f"LINKS: {cnt}")

        # session.commit()
        logger.info("Creating links FINISH")


def delete_data() -> None:
    logger.info("Deleting data")
    with db.session_factory() as session:
        session.query(User).delete()
        session.query(ReferalLink).delete()
        session.commit()

    logger.info("Deleting data FINISH")


def main():
    users = get_data("data/fixtures/json_users.json")
    invoices = get_data("data/fixtures/json_invoices.json")
    links = get_data("data/fixtures/json_links.json")

    create_users(users, invoices)
    create_links(links, users, invoices)


def save_errors():
    with open("errors.log", "w") as file:
        file.write("\n".join(errors))


if __name__ == '__main__':
    delete_data()
    main()
    save_errors()
