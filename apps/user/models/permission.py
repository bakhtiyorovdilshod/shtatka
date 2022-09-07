import sqlalchemy
from apps.user.models.base import base_model
from apps.user.models import metadata

BASE_FIELDS = base_model()

FIELDS = [
    *BASE_FIELDS,
    sqlalchemy.Column('name', sqlalchemy.String(255))

]

PermissionTable = sqlalchemy.Table(
    'permissions',  metadata, *FIELDS
)


__all__ = ['metadata', 'PermissionTable']