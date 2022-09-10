"""fixed

Revision ID: 817b1edc97fe
Revises: db96a3431079
Create Date: 2022-09-10 18:50:08.994067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '817b1edc97fe'
down_revision = 'db96a3431079'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client_department_positions',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('created_date', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('count', sa.INTEGER(), nullable=False),
    sa.Column('base_salary', sa.INTEGER(), nullable=False),
    sa.Column('bonus_salary', sa.INTEGER(), nullable=False),
    sa.Column('minimal_salary', sa.INTEGER(), nullable=False),
    sa.Column('other_bonus_salary', sa.INTEGER(), nullable=False),
    sa.Column('razryad_coefficient', sa.INTEGER(), nullable=False),
    sa.Column('razryad_value', sa.INTEGER(), nullable=False),
    sa.Column('razryad_subtract', sa.INTEGER(), nullable=False),
    sa.Column('client_department_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['client_department_id'], ['client_departments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('client_department_positions')
    # ### end Alembic commands ###
