from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Tariff(Base):
    __tablename__ = "tariffs"

    name: Mapped[str] = mapped_column(String(50))
    code: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    chatgpt_daily_limit: Mapped[int]
    dalle_2_daily_limit: Mapped[int]
    sd_daily_limit: Mapped[int]
    token_balance: Mapped[int]
    days: Mapped[int]
    price: Mapped[int]
    main_tariff_id: Mapped[int | None] = mapped_column(default=None, unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_extra: Mapped[bool] = mapped_column(default=False)
    is_trial: Mapped[bool] = mapped_column(default=False)

    users: Mapped[list["User"]] = relationship(back_populates="tariff")
    invoices: Mapped["Invoice"] = relationship(back_populates="tariff")

    def __str__(self):
        return f"<Tariff: {self.name}>"


class Invoice(Base):
    __tablename__ = "invoices"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    is_paid: Mapped[bool] = mapped_column(default=False)
    mother_invoice_id: Mapped[int | None] = mapped_column(default=None)
    tariff_id: Mapped[int] = mapped_column(ForeignKey("tariffs.id"))

    user: Mapped["User"] = relationship(back_populates="invoices")
    tariff: Mapped["Tariff"] = relationship(back_populates="invoices")

    def __str__(self):
        return f"<Invoice: {self.id} | User: {self.user_id}>"
