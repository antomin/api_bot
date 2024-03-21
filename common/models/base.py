from datetime import datetime

from sqlalchemy import DateTime, create_engine, BigInteger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.sql.functions import now


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now(), server_default=now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=now(), server_default=now(), onupdate=now())


class Database:
    def __init__(self, url: str, echo: bool = False):
        self.async_engine = create_async_engine(url=url, echo=echo)
        self.engine = create_engine(url=url, echo=echo)
        self.async_session_factory = async_sessionmaker(
            bind=self.async_engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
        self.session_factory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

