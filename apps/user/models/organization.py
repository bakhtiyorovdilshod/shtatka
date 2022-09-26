import sqlalchemy, enum
from sqlalchemy import func

from apps.user.models.base import base_model
from apps.user.models import metadata

BASE_FIELDS = base_model()

ORGANIZATION_FIELDS = [
    *BASE_FIELDS,
    sqlalchemy.Column('name', sqlalchemy.String(255)),
    sqlalchemy.Column('organization_tin', sqlalchemy.String(80), unique=True),

]


class StatusChoice(enum.Enum):
    pending = 'pending'
    checked = 'checked'
    approved = 'approved'
    confirmed = 'confirmed'
    finished = 'finished'


class TypeChoice(enum.Enum):
    with_self = 'with_self'
    with_budget = 'with_budget'


FIELDS = [
    sqlalchemy.Column('id', sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column('created_date', sqlalchemy.DateTime, server_default=func.now()),
    sqlalchemy.Column('child_name', sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column('address', sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column('chapter_code', sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column('department_code', sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column('small_department_code', sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column('is_main', sqlalchemy.Boolean(), default=False),
    sqlalchemy.Column('client_shtatka_id', sqlalchemy.ForeignKey('client_shtatkas.id'), nullable=False)

]


CLIENT_SHTATKA_FIELDS = [
    sqlalchemy.Column('id', sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column('created_date', sqlalchemy.DateTime, server_default=func.now()),
    sqlalchemy.Column('parent_id', sqlalchemy.ForeignKey('shtat_organizations.id'), nullable=False),
    sqlalchemy.Column('status', sqlalchemy.Enum(StatusChoice), default='pending'),
    sqlalchemy.Column('shtatka_status', sqlalchemy.String(50), default='pending'),
    sqlalchemy.Column('type', sqlalchemy.Enum(TypeChoice), nullable=False)

]


ClientShtatkaTable = sqlalchemy.Table(
    'client_shtatkas', metadata, *CLIENT_SHTATKA_FIELDS
)
OrganizationTable = sqlalchemy.Table(
    'shtat_organizations', metadata, *ORGANIZATION_FIELDS
)


OrganizationChildTable = sqlalchemy.Table(
    'organization_children', metadata, *FIELDS
)


__all__ = ['metadata', 'OrganizationTable', 'OrganizationChildTable', 'ClientShtatkaTable']