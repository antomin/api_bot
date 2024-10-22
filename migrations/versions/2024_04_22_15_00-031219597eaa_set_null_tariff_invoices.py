"""SET NULL Tariff-Invoices

Revision ID: 031219597eaa
Revises: 24530c5a4f5d
Create Date: 2024-04-22 15:00:40.919318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '031219597eaa'
down_revision = '24530c5a4f5d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invoices', schema=None) as batch_op:
        batch_op.alter_column('tariff_id',
               existing_type=sa.BIGINT(),
               nullable=True)
        batch_op.drop_constraint('invoices_user_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('invoices_tariff_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'], ondelete='SET NULL')
        batch_op.create_foreign_key(None, 'tariffs', ['tariff_id'], ['id'], ondelete='SET NULL')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invoices', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('invoices_tariff_id_fkey', 'tariffs', ['tariff_id'], ['id'])
        batch_op.create_foreign_key('invoices_user_id_fkey', 'users', ['user_id'], ['id'], ondelete='CASCADE')
        batch_op.alter_column('tariff_id',
               existing_type=sa.BIGINT(),
               nullable=False)

    # ### end Alembic commands ###
