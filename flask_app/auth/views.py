from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import login_user, logout_user, current_user, login_required
from flask_app.forms import LoginForm
from common.models.user import UserAdmin


auth_app = Blueprint("auth_app", __name__)


@auth_app.route('/admin/login/', methods=['GET', 'POST'], endpoint="login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.index"))

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = UserAdmin.query.filter_by(username=form.username.data).one_or_none()
        if user is None:
            return render_template("auth/login.html", form=form, error="username doesn't exist")
        if not user.check_password(form.password.data):
            return render_template("auth/login.html", form=form, error="unvalid username or password")

        login_user(user)
        return redirect(url_for("admin.index"))

    return render_template("auth/login.html", form=form)