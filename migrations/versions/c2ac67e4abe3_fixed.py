"""fixed

Revision ID: c2ac67e4abe3
Revises: aa380e7c8670
Create Date: 2022-09-11 01:19:53.972456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2ac67e4abe3'
down_revision = 'aa380e7c8670'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('client_departments', 'total_base_salary',
               existing_type=sa.INTEGER(),
               type_=sa.DECIMAL(precision=15, scale=2),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('client_departments', 'total_base_salary',
               existing_type=sa.DECIMAL(precision=15, scale=2),
               type_=sa.INTEGER(),
               existing_nullable=False)
    # ### end Alembic commands ###
