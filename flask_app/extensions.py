from flask_admin import Admin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from common.models import Base
from common.settings import settings

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
admin = Admin(name=settings.APP_NAME, template_mode="bootstrap4")
