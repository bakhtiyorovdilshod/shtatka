"""username and password have been added to the user model

Revision ID: d20f5d3050a2
Revises: bfe059feeebf
Create Date: 2022-08-31 09:18:32.484940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd20f5d3050a2'
down_revision = 'bfe059feeebf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.String(length=52), nullable=False))
    op.add_column('users', sa.Column('password', sa.String(length=92), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password')
    op.drop_column('users', 'username')
    # ### end Alembic commands ###