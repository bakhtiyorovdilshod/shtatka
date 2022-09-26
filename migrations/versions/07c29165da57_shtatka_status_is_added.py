"""shtatka status is added

Revision ID: 07c29165da57
Revises: 44db2275fc7f
Create Date: 2022-09-26 16:45:32.166026

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '07c29165da57'
down_revision = '44db2275fc7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    type_choice_enum = postgresql.ENUM('with_self', 'with_budget', name='typechoice', create_type=False)
    type_choice_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('client_shtatkas', sa.Column('shtatka_status', sa.String(length=50), nullable=True))
    op.alter_column('client_shtatkas', 'type',
               existing_type=type_choice_enum,
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('client_shtatkas', 'type',
               existing_type=postgresql.ENUM('with_self', 'with_budget', name='typechoice'),
               nullable=True)
    op.drop_column('client_shtatkas', 'shtatka_status')
    # ### end Alembic commands ###
