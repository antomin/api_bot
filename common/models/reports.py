# from typing import TYPE_CHECKING
#
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from common.models import Base
#
# if TYPE_CHECKING:
#     from .user import User
#
#
# class GenerationLog(Base):
#     __tablename__ = "generation_logs"
#
#     user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
#     type: Mapped[str]
#
#     user: Mapped["User"] = relationship(back_populates="services")
#
#     def __str__(self):
#         return ''
