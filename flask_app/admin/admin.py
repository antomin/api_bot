from flask_admin.contrib.sqla import ModelView

from common.models import User, ReferalLink, Tariff, Invoice, TextQuery, TextGenerationRole, ImageQuery, VideoQuery
from flask_app.extensions import admin, db


class AdminView(ModelView):
    pass


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
