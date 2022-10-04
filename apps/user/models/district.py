import sqlalchemy
from apps.user.models.base import base_model
from apps.user.models import metadata

BASE_FIELDS = base_model()


FIELDS = [
    *BASE_FIELDS,
    sqlalchemy.Column('name', sqlalchemy.String(255)),
    sqlalchemy.Column('client_shtatka_region_id', sqlalchemy.ForeignKey('client_shtatka_regions.id'))

]

ClientShtatkaDistrictTable = sqlalchemy.Table(
    'client_shtatka_districts', metadata, *FIELDS
)

__all__ = ['metadata', 'ClientShtatkaDistrictTable']





