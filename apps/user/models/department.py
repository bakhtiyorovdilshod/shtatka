import enum

import sqlalchemy, copy
from sqlalchemy import func

from apps.user.models.base import base_model
from apps.user.models import metadata

BASE_FIELDS = base_model()


class TypeChoice(enum.Enum):
    with_self = 'with_self'
    with_budget = 'with_budget'


SHTAT_DEPARTMENT_FIELDS = [
    sqlalchemy.Column('id', sqlalchemy.INTEGER, primary_key=True, autoincrement=True),
    sqlalchemy.Column('name', sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column('code', sqlalchemy.String(80), nullable=False, unique=True),

]

SHTAT_DEPARTMENT_ORGANIZATION_FIELDS = [
    sqlalchemy.Column('id', sqlalchemy.INTEGER, primary_key=True, autoincrement=True),
    sqlalchemy.Column('shtat_department_id', sqlalchemy.ForeignKey('shtat_departments.id', ondelete="CASCADE"), nullable=False),
    sqlalchemy.Column('organization_id', sqlalchemy.ForeignKey('shtat_organizations.id'), nullable=False),
    sqlalchemy.Column('type', sqlalchemy.Enum(TypeChoice), nullable=False)

]


SHTAT_DEPARTMENT_USER_FIELDS = [
    sqlalchemy.Column('id', sqlalchemy.INTEGER, primary_key=True, autoincrement=True),
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey('users.id', ondelete="CASCADE"), nullable=False),
    sqlalchemy.Column('shtat_department_id', sqlalchemy.ForeignKey('shtat_departments.id', ondelete="CASCADE"), nullable=False),

]

CLIENT_DEPARTMENT_FIELDS = [
    sqlalchemy.Column('id', sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column('created_date', sqlalchemy.DateTime, server_default=func.now()),
    sqlalchemy.Column('name', sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column('total_count', sqlalchemy.INTEGER, nullable=False),
    sqlalchemy.Column('total_minimal_salary', sqlalchemy.DECIMAL(15, 2), nullable=False),
    sqlalchemy.Column('total_bonus_salary', sqlalchemy.DECIMAL(15, 2), nullable=False),
    sqlalchemy.Column('total_base_salary', sqlalchemy.DECIMAL(15, 2), nullable=False),
    sqlalchemy.Column('child_id', sqlalchemy.ForeignKey('organization_children.id'), nullable=False)
]

ClientDepartmentTable = sqlalchemy.Table(
    'client_departments', metadata, *CLIENT_DEPARTMENT_FIELDS
)


ShtatDepartmentTable = sqlalchemy.Table(
    'shtat_departments',  metadata, *SHTAT_DEPARTMENT_FIELDS
)


ShtatDepartmentOrganizationTable = sqlalchemy.Table(
    'shtat_department_organizations', metadata, *SHTAT_DEPARTMENT_ORGANIZATION_FIELDS
)

ShtatDepartmentUser = sqlalchemy.Table(
    'shtat_department_users', metadata, *SHTAT_DEPARTMENT_USER_FIELDS
)

__all__ = ['metadata', 'ShtatDepartmentTable', 'ShtatDepartmentOrganizationTable', 'ShtatDepartmentUser', 'ClientDepartmentTable']