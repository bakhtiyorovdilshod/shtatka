"""permission is added

Revision ID: a5749354a4c1
Revises: 4f4cbd48f849
Create Date: 2022-09-07 17:47:40.514241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5749354a4c1'
down_revision = '4f4cbd48f849'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'shtat_organizations', ['organization_tin'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'shtat_organizations', type_='unique')
    # ### end Alembic commands ###