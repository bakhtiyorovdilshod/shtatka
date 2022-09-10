import sqlalchemy
metadata = sqlalchemy.MetaData()

from apps.user.models.role import *
from apps.user.models.user import *
from apps.user.models.organization import *
from apps.user.models.department import *
from apps.user.models.permission import *
from apps.user.models.position import *