from flask import Blueprint, render_template

main_app = Blueprint(name="landing", import_name=__name__, url_prefix="/")


@main_app.get("/")
def index():
    return render_template("user_templates/index.html")


@main_app.get("/policy/")
def policy():
    return render_template("user_templates/policy.html")


@main_app.get("/offer/")
def offer():
    return render_template("user_templates/offer.html")
