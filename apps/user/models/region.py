import sqlalchemy
from apps.user.models.base import base_model
from apps.user.models import metadata

BASE_FIELDS = base_model()


FIELDS = [
    *BASE_FIELDS,
    sqlalchemy.Column('name', sqlalchemy.String(255)),
    sqlalchemy.Column('organization_child_id', sqlalchemy.ForeignKey('organization_children.id'))

]

ClientShtatkaRegionTable = sqlalchemy.Table(
    'client_shtatka_regions', metadata, *FIELDS
)

__all__ = ['metadata', 'ClientShtatkaRegionTable']
