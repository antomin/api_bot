"""Add chatgpt_daili_limit

Revision ID: f87bfbce9771
Revises: 031219597eaa
Create Date: 2024-04-25 19:25:57.571105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f87bfbce9771'
down_revision = '031219597eaa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reports',
    sa.Column('Всего пользователей', sa.Integer(), nullable=False),
    sa.Column('Пользователей с реф. ссылок', sa.Integer(), nullable=False),
    sa.Column('Новых пользователей', sa.Integer(), nullable=False),
    sa.Column('Новых пользователей с реф. ссылок', sa.Integer(), nullable=False),
    sa.Column('Новых пользователей с поиска', sa.Integer(), nullable=False),
    sa.Column('Кол-во запросов', sa.Integer(), nullable=False),
    sa.Column('Кол-во запросов ChatGPT 3', sa.Integer(), nullable=False),
    sa.Column('Кол-во запросов ChatGPT 4', sa.Integer(), nullable=False),
    sa.Column('Кол-во запросов YaGPT', sa.Integer(), nullable=False),
    sa.Column('Кол-во запросов YaGPT Lite', sa.Integer(), nullable=False),
    sa.Column('Кол-во запросов Gemini', sa.Integer(), nullable=False),
    sa.Column('Кол-во запросов Claude', sa.Integer(), nullable=False),
    sa.Column('Кол-во запросов StableDiffusion', sa.Integer(), nullable=False),
    sa.Column('Кол-во запросов DALL-E-2', sa.Integer(), nullable=False),
    sa.Column('Кол-во запросов DALL-E-3', sa.Integer(), nullable=False),
    sa.Column('Кол-во запросов Midjourney', sa.Integer(), nullable=False),
    sa.Column('Кол-во запросов Kandinsky', sa.Integer(), nullable=False),
    sa.Column('Кол-во генераций текст в видео', sa.Integer(), nullable=False),
    sa.Column('Кол-во генераций картинка в видео', sa.Integer(), nullable=False),
    sa.Column('Кол-во удаления фона с видео', sa.Integer(), nullable=False),
    sa.Column('Кол-во генераций видео в мульт', sa.Integer(), nullable=False),
    sa.Column('Кол-во генераций PicaArt', sa.Integer(), nullable=False),
    sa.Column('Кол-во генераций дипломов', sa.Integer(), nullable=False),
    sa.Column('Кол-во рерайта', sa.Integer(), nullable=False),
    sa.Column('Кол-во решений по фото', sa.Integer(), nullable=False),
    sa.Column('Кол-во генераций статей', sa.Integer(), nullable=False),
    sa.Column('Кол-во озвучек', sa.Integer(), nullable=False),
    sa.Column('Кол-во речь в текст', sa.Integer(), nullable=False),
    sa.Column('Кол-во удаления фона с картинок', sa.Integer(), nullable=False),
    sa.Column('Кол-во премиум пользователей', sa.Integer(), nullable=False),
    sa.Column('Кол-во новых оплат премиума', sa.Integer(), nullable=False),
    sa.Column('Сумма новых оплат премиума', sa.Integer(), nullable=False),
    sa.Column('Кол-во новых оплат токенов', sa.Integer(), nullable=False),
    sa.Column('Сумма новых оплат токенов', sa.Integer(), nullable=False),
    sa.Column('Кол-во новых оплат', sa.Integer(), nullable=False),
    sa.Column('Сумма новых оплат', sa.Integer(), nullable=False),
    sa.Column('Средний чек', sa.Integer(), nullable=False),
    sa.Column('Кол-во покупок триала', sa.Integer(), nullable=False),
    sa.Column('Кол-во покупок по тарифам', sa.JSON(), nullable=False),
    sa.Column('Кол-во продлений', sa.Integer(), nullable=False),
    sa.Column('Дата', sa.Date(), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('tariffs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('chatgpt_daily_limit', sa.Integer(), nullable=True))

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('chatgpt_daily_limit', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('chatgpt_daily_limit')

    with op.batch_alter_table('tariffs', schema=None) as batch_op:
        batch_op.drop_column('chatgpt_daily_limit')

    op.drop_table('reports')
    # ### end Alembic commands ###
