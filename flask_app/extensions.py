from flask_admin import Admin
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from common.models import Base
from common.settings import settings
from flask_app import MyAdminIndexView

db = SQLAlchemy(model_class=Base)
migrate = Migrate(compare_type=True)
admin = Admin(name=settings.APP_NAME, index_view=MyAdminIndexView(), template_mode="bootstrap4", base_template='master-extended.html')
login_manager = LoginManager()

__all__ = ["db", "migrate", "login_manager", "admin"]
