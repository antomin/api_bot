import click
from flask.cli import AppGroup
from flask_app.extensions import db
from common.models.user import UserAdmin

admin_cli = AppGroup('admin')

@admin_cli.command('create-admin')
@click.argument('username')
@click.argument('password')
def create_admin(username, password):
    admin = UserAdmin(username=username)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    print(f'Admin user {username} created successfully.')
