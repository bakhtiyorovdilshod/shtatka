import sqlalchemy, copy
from sqlalchemy.sql import func

from apps.user.models.base import base_model
from apps.user.models import metadata

BASE_FIELDS = base_model()


CLIENT_DEPARTMENT_POSITION_FIELDS = [
    *BASE_FIELDS,
    sqlalchemy.Column('name', sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column('count', sqlalchemy.INTEGER, nullable=False),
    sqlalchemy.Column('base_salary', sqlalchemy.DECIMAL(15, 2), nullable=False),
    sqlalchemy.Column('bonus_salary', sqlalchemy.DECIMAL(15, 2), nullable=False),
    sqlalchemy.Column('minimal_salary', sqlalchemy.DECIMAL(15, 2), nullable=False),
    sqlalchemy.Column('other_bonus_salary', sqlalchemy.DECIMAL(15, 2), nullable=False),
    sqlalchemy.Column('razryad_coefficient', sqlalchemy.DECIMAL(5, 3), nullable=False),
    sqlalchemy.Column('razryad_value', sqlalchemy.DECIMAL(15, 2), nullable=False),
    sqlalchemy.Column('razryad_subtract', sqlalchemy.INTEGER, nullable=False),
    sqlalchemy.Column('client_department_id', sqlalchemy.ForeignKey('client_departments.id'), nullable=False)

]

ClientDepartmentPositionTable = sqlalchemy.Table(
    'client_department_positions', metadata, *CLIENT_DEPARTMENT_POSITION_FIELDS
)

__all__ = ['metadata', 'ClientDepartmentPositionTable']