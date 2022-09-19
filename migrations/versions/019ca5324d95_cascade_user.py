"""cascade user

Revision ID: 019ca5324d95
Revises: c2a2a7a67afe
Create Date: 2022-09-19 21:36:09.503014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '019ca5324d95'
down_revision = 'c2a2a7a67afe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('shtat_department_users_user_id_fkey', 'shtat_department_users', type_='foreignkey')
    op.create_foreign_key(None, 'shtat_department_users', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'shtat_department_users', type_='foreignkey')
    op.create_foreign_key('shtat_department_users_user_id_fkey', 'shtat_department_users', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###