"""removed organization_shtatka

Revision ID: 42cc407de231
Revises: 7a3e7f4068e3
Create Date: 2022-09-13 01:32:57.312703

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '42cc407de231'
down_revision = '7a3e7f4068e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('organization_shtatka')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('organization_shtatka',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_date', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('parent_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('status', postgresql.ENUM('pending', 'approved', 'confirmed', name='statuschoice'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['shtat_organizations.id'], name='organization_shtatka_parent_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='organization_shtatka_pkey')
    )
    # ### end Alembic commands ###
