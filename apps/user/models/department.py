import sqlalchemy, copy

from apps.user.models.base import base_model
from apps.user.models import metadata

BASE_FIELDS = base_model()

SHTAT_DEPARTMENT_FIELDS = [
    sqlalchemy.Column('id', sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String(255)),
    sqlalchemy.Column('code', sqlalchemy.String(80)),

]

SHTAT_DEPARTMENT_ORGANIZATION_FIELDS = [
    sqlalchemy.Column('id', sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column('shtat_department_id', sqlalchemy.ForeignKey('shtat_departments.id')),
    sqlalchemy.Column('organization_id', sqlalchemy.ForeignKey('shtat_organizations.id')),

]


SHTAT_DEPARTMENT_USER_FIELDS = [
    sqlalchemy.Column('id', sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('shtat_department_id', sqlalchemy.ForeignKey('shtat_departments.id')),

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