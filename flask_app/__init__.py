import flask_login as login
from flask import redirect, url_for
from flask_admin import AdminIndexView, expose
from flask_login import current_user, logout_user


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('auth_app.login'))
        return self.render('admin/index.html', title='Admin Panel')

    @expose('/logout/')
    def logout_page(self):
        login.logout_user()
        return redirect(url_for('admin.index'))
