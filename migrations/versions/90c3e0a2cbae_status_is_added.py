"""status is added

Revision ID: 90c3e0a2cbae
Revises: 1408d89c40b8
Create Date: 2022-09-10 23:48:57.447956

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '90c3e0a2cbae'
down_revision = '1408d89c40b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    status_choice_enum = postgresql.ENUM('pending', 'approved', 'confirmed', name='statuschoice', create_type=False)
    status_choice_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('client_department_positions', sa.Column('right_coefficient', sa.DECIMAL(precision=5, scale=3), nullable=True))
    op.add_column('organization_children', sa.Column('status', status_choice_enum, nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('organization_children', 'status')
    op.drop_column('client_department_positions', 'right_coefficient')
    # ### end Alembic commands ###
