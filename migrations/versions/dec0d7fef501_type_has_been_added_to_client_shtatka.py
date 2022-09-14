"""type has been added to client_shtatka

Revision ID: dec0d7fef501
Revises: 42cc407de231
Create Date: 2022-09-13 14:09:24.066142

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'dec0d7fef501'
down_revision = '42cc407de231'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    type_choice_enum = postgresql.ENUM('with_self', 'with_budget', name='typechoice', create_type=False)
    type_choice_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('client_shtatkas', sa.Column('type', type_choice_enum, nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('client_shtatkas', 'type')
    # ### end Alembic commands ###