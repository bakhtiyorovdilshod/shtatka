import sqlalchemy

from apps.user.models.base import base_model
from apps.user.models import metadata

BASE_FIELDS = base_model()

ORGANIZATION_FIELDS = [
    *BASE_FIELDS,
    sqlalchemy.Column('name', sqlalchemy.String(255)),
    sqlalchemy.Column('organization_tin', sqlalchemy.String(80)),

]


OrganizationTable = sqlalchemy.Table(
    'shtat_organizations', metadata, *ORGANIZATION_FIELDS
)

__all__ = ['metadata', 'OrganizationTable']