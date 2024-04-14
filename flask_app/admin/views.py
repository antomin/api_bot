from flask_admin import expose, AdminIndexView
from flask_login import current_user, logout_user
from flask import url_for, redirect, request
import flask_login as login
import json
from flask_app.forms import EditForm
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from flask_admin.form import rules


def update_json(data):
    result = {}
    for key, value in data.items():
        result[key] = value
    with open('../common/settings.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)


class MyAdminIndexView(AdminIndexView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('auth_app.login'))
        form = EditForm()

        if request.method == 'POST' and form.validate_on_submit():
            update_json(request.form)

        with open('../common/settings.json', 'r') as json_file:
            data = json.load(json_file)

        return self.render('admin/index.html', title='Admin Panel', data=data, form=form)

    @expose('/logout/')
    def logout_page(self):
        login.logout_user()
        return redirect(url_for('admin.index'))
