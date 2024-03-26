from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models import Base

from ..enums import ImageModels, TextModels, VideoTypes

if TYPE_CHECKING:
    from .user import User


class TextSession(Base):
    __tablename__ = "sessions"

    name: Mapped[str | None]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_active: Mapped[bool] = mapped_column(default=True)

    user: Mapped["User"] = relationship(back_populates="sessions")
    text_queries: Mapped[list["TextQuery"]] = relationship(back_populates="session")

    def __str__(self):
        return f"<Session: {self.id}>"


class TextQuery(Base):
    __tablename__ = "text_queries"

    model: Mapped[TextModels] = mapped_column(String(20), default=TextModels.GPT_3_TURBO)
    session_id: Mapped[int | None] = mapped_column(ForeignKey("sessions.id", ondelete="SET NULL"))
    prompt: Mapped[str]
    result: Mapped[str]

    session: Mapped["TextSession"] = relationship(back_populates="text_queries")

    def __str__(self):
        return f"<TextQuery: {self.model} | {self.id}({self.session_id})"


class ImageQuery(Base):
    __tablename__ = "image_queries"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    model: Mapped[ImageModels] = mapped_column(String(20), default=ImageModels.STABLE_DIFFUSION)
    prompt: Mapped[str]
    result: Mapped[str]

    user: Mapped["User"] = relationship(back_populates="image_queries")

    def __str__(self):
        return f"<ImageQuery | {self.model}: <{self.id}>"


class VideoQuery(Base):
    __tablename__ = "video_queries"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    type: Mapped[VideoTypes] = mapped_column(String(20))
    prompt: Mapped[str]
    result: Mapped[str]

    user: Mapped["User"] = relationship(back_populates="video_queries")

    def __str__(self):
        return f"<VideoQuery | {self.type}: <{self.id}>"


class ServiceQuery(Base):
    __tablename__ = "service_queries"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    type: Mapped[str] = mapped_column(String(20))

    user: Mapped["User"] = relationship(back_populates="services_queries")


class TextGenerationRole(Base):
    __tablename__ = "text_generation_roles"

    title: Mapped[str] = mapped_column(unique=True)
    prompt: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(default=True)

    users: Mapped[list["User"]] = relationship(back_populates="txt_model_role")

    def __repr__(self):
        return f"<TextRole | {self.title}>"
