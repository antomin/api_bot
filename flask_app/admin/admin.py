import flask_login as login
from flask import redirect, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user

from common.models import (ImageQuery, Invoice, ReferalLink, Tariff,
                           TextGenerationRole, TextQuery, User, VideoQuery)
from flask_app.extensions import admin, db


class AdminView(ModelView):
    pass
    # def is_accessible(self):
    #     return current_user.is_authenticated
    #
    # def inaccessible_callback(self, name, **kwargs):
    #     # Redirect to login page if user is not authenticated
    #     return redirect(url_for('login', next=request.url))


class UserAdminView(AdminView):
    column_display_pk = True
    can_create = True
    form_columns = ['id', 'username', 'first_name', 'last_name']


class ReferalLinkView(AdminView):
    pass


class TariffView(AdminView):
    pass


class InvoiceView(AdminView):
    pass


class TextQueryView(AdminView):
    pass


class TextGenerationRoleView(AdminView):
    pass


class ImageQueryView(AdminView):
    pass


class VideoQueryView(AdminView):
    pass


admin.add_view(UserAdminView(User, db.session, name='Пользователи'))
admin.add_view(ReferalLinkView(ReferalLink, db.session))
admin.add_view(TariffView(Tariff, db.session))
admin.add_view(InvoiceView(Invoice, db.session))
admin.add_view(TextQueryView(TextQuery, db.session))
admin.add_view(TextGenerationRoleView(TextGenerationRole, db.session))
admin.add_view(ImageQueryView(ImageQuery, db.session))
admin.add_view(VideoQueryView(VideoQuery, db.session))
