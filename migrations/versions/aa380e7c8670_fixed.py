"""fixed

Revision ID: aa380e7c8670
Revises: 90c3e0a2cbae
Create Date: 2022-09-11 01:16:57.638760

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa380e7c8670'
down_revision = '90c3e0a2cbae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('client_department_positions', 'base_salary',
               existing_type=sa.INTEGER(),
               type_=sa.DECIMAL(precision=15, scale=2),
               existing_nullable=False)
    op.alter_column('client_department_positions', 'bonus_salary',
               existing_type=sa.INTEGER(),
               type_=sa.DECIMAL(precision=15, scale=2),
               existing_nullable=False)
    op.alter_column('client_department_positions', 'minimal_salary',
               existing_type=sa.INTEGER(),
               type_=sa.DECIMAL(precision=15, scale=2),
               existing_nullable=False)
    op.alter_column('client_department_positions', 'other_bonus_salary',
               existing_type=sa.INTEGER(),
               type_=sa.DECIMAL(precision=15, scale=2),
               existing_nullable=False)
    op.alter_column('client_department_positions', 'razryad_coefficient',
               existing_type=sa.INTEGER(),
               type_=sa.DECIMAL(precision=5, scale=3),
               existing_nullable=False)
    op.alter_column('client_departments', 'total_minimal_salary',
               existing_type=sa.INTEGER(),
               type_=sa.DECIMAL(precision=15, scale=2),
               existing_nullable=False)
    op.alter_column('client_departments', 'total_bonus_salary',
               existing_type=sa.INTEGER(),
               type_=sa.DECIMAL(precision=15, scale=2),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('client_departments', 'total_bonus_salary',
               existing_type=sa.DECIMAL(precision=15, scale=2),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('client_departments', 'total_minimal_salary',
               existing_type=sa.DECIMAL(precision=15, scale=2),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('client_department_positions', 'razryad_coefficient',
               existing_type=sa.DECIMAL(precision=5, scale=3),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('client_department_positions', 'other_bonus_salary',
               existing_type=sa.DECIMAL(precision=15, scale=2),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('client_department_positions', 'minimal_salary',
               existing_type=sa.DECIMAL(precision=15, scale=2),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('client_department_positions', 'bonus_salary',
               existing_type=sa.DECIMAL(precision=15, scale=2),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('client_department_positions', 'base_salary',
               existing_type=sa.DECIMAL(precision=15, scale=2),
               type_=sa.INTEGER(),
               existing_nullable=False)
    # ### end Alembic commands ###
