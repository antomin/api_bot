from flask import Blueprint, render_template

main_app = Blueprint(name="landing", import_name=__name__, url_prefix="/")


@main_app.get("/")
def index():
    return render_template("main_index.html")
