import sqlalchemy, copy

from apps.user.models.base import base_model
from apps.user.models import metadata

BASE_FIELDS = base_model()

SHTAT_DEPARTMENT_FIELDS = [
    sqlalchemy.Column('id', sqlalchemy.INTEGER, primary_key=True, autoincrement=True),
    sqlalchemy.Column('name', sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column('code', sqlalchemy.String(80), nullable=False, unique=True),

]

SHTAT_DEPARTMENT_ORGANIZATION_FIELDS = [
    sqlalchemy.Column('id', sqlalchemy.INTEGER, primary_key=True, autoincrement=True),
    sqlalchemy.Column('shtat_department_id', sqlalchemy.ForeignKey('shtat_departments.id', ondelete="CASCADE"), nullable=False),
    sqlalchemy.Column('organization_id', sqlalchemy.ForeignKey('shtat_organizations.id'), nullable=False),

]


SHTAT_DEPARTMENT_USER_FIELDS = [
    sqlalchemy.Column('id', sqlalchemy.INTEGER, primary_key=True, autoincrement=True),
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey('users.id'), nullable=False),
    sqlalchemy.Column('shtat_department_id', sqlalchemy.ForeignKey('shtat_departments.id', ondelete="CASCADE"), nullable=False),

]


ShtatDepartmentTable = sqlalchemy.Table(
    'shtat_departments',  metadata, *SHTAT_DEPARTMENT_FIELDS
)


ShtatDepartmentOrganizationTable = sqlalchemy.Table(
    'shtat_department_organizations', metadata, *SHTAT_DEPARTMENT_ORGANIZATION_FIELDS
)

ShtatDepartmentUser = sqlalchemy.Table(
    'shtat_department_users', metadata, *SHTAT_DEPARTMENT_USER_FIELDS
)

__all__ = ['metadata', 'ShtatDepartmentTable', 'ShtatDepartmentOrganizationTable', 'ShtatDepartmentUser']