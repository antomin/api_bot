from flask import Flask

from common.settings import settings
from flask_app.admin.admin import admin
from flask_app.auth.views import auth_app
from flask_app.commands.create_superuser import admin_cli
from flask_app.extensions import db, login_manager, migrate
from flask_app.main_app.views import main_app
from flask_app.payments_app.views import payments_app


def __register_blueprints(app: Flask) -> None:
    app.register_blueprint(main_app)
    app.register_blueprint(auth_app)
    app.register_blueprint(payments_app)


def __set_settings(app: Flask) -> None:
    app.config["FLASK_ENV"] = "development" if settings.DEBUG else "production"
    app.config["DEBUG"] = settings.DEBUG
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DB_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings.DEBUG
    app.config["SECRET_KEY"] = settings.SECRET_KEY


def __set_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    admin.init_app(app=app)
    login_manager.init_app(app)


def create_app() -> Flask:
    app = Flask(__name__, static_url_path="/static", static_folder="flask_app/static")

    __set_settings(app)
    __set_extensions(app)
    __register_blueprints(app)

    app.cli.add_command(admin_cli)

    return app
