from .base import Base, Database
from .user import User, ReferalLink
from .generations import TextQuery, ImageQuery, VideoQuery
from .payments import Tariff, Invoice
from ..settings import settings

db = Database(url=settings.ASYNC_DB_URL)
