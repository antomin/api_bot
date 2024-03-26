from ..settings import settings
from .base import Base, Database
from .generations import ImageQuery, TextGenerationRole, TextQuery, VideoQuery
from .payments import Invoice, Tariff
from .user import ReferalLink, User

db = Database(url=settings.ASYNC_DB_URL)
