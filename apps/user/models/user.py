import sqlalchemy

from apps.user.models.base import base_model
from apps.user.models import metadata

BASE_FIELDS = base_model()

FIELDS = [
    *BASE_FIELDS,
    sqlalchemy.Column('full_name', sqlalchemy.String(255)),
    sqlalchemy.Column('pinfl', sqlalchemy.String(80)),
    sqlalchemy.Column('role_id', sqlalchemy.ForeignKey('user_roles.id'))

]

UserTable = sqlalchemy.Table(
    'users',  metadata, *FIELDS
)


__all__ = ['metadata', 'UserTable']