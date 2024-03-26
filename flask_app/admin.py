from flask_admin.contrib.sqla import ModelView

from common.models import User
from flask_app.extensions import admin, db


class AdminView(ModelView):
    pass


class UserAdminView(AdminView):
    pass


admin.add_view(UserAdminView(User, db.session))
