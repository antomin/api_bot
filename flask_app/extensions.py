from flask_admin import Admin, helpers
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_app.admin.views import MyAdminIndexView
# from flask_security import Security
# from flask_app.adminlte.admin import AdminLte, admins_store
# from flask import url_for


from common.models import Base
from common.settings import settings
from flask_app import MyAdminIndexView

db = SQLAlchemy(model_class=Base)
migrate = Migrate(compare_type=True)
login_manager = LoginManager()
# security = Security(datastore=admins_store)
admin = Admin(name=settings.APP_NAME, index_view=MyAdminIndexView(), template_mode="bootstrap4", base_template='master-extended.html')
# admin = AdminLte(skin='green', name=settings.APP_NAME, short_name="<b>F</b>C", long_name="<b>Flask</b>CMS", base_template='master-extended.html', index_view=MyAdminIndexView())


# @security.context_processor
# def security_context_processor():
#     return dict(
#         admin_base_template=admin.base_template,
#         admin_view=admin.index_view,
#         h=helpers,
#         get_url=url_for
#     )


__all__ = ["db", "migrate", "login_manager", "admin"]
