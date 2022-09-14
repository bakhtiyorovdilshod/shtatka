"""type has been added to shtat_department_organizations

Revision ID: c2a2a7a67afe
Revises: dec0d7fef501
Create Date: 2022-09-13 14:40:13.435743

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c2a2a7a67afe'
down_revision = 'dec0d7fef501'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    type_choice_enum = postgresql.ENUM('with_self', 'with_budget', name='typechoice', create_type=False)
    type_choice_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('shtat_department_organizations', sa.Column('type', type_choice_enum, nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shtat_department_organizations', 'type')
    # ### end Alembic commands ###