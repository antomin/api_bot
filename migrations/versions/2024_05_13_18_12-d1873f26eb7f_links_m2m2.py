"""links m2m2

Revision ID: d1873f26eb7f
Revises: f63b1655ddc5
Create Date: 2024-05-13 18:12:03.855556

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'd1873f26eb7f'
down_revision = 'f63b1655ddc5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_referral_link_association',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('referal_link_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['referal_link_id'], ['referal_links.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'referal_link_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_referral_link_association')
    # ### end Alembic commands ###