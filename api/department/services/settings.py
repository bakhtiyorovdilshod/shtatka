from fastapi import HTTPException

from api.department.schemas.settings import GivePermissionSchema
from api.user.utils.queryset import Queryset
from core.settings import database


class DepartmentSettingsService:

    @staticmethod
    def give_permission(data: GivePermissionSchema):
        query = 'SELECT id FROM permissions WHERE id= :permission_id'
        row = database.fetch_one(query=query, values={'permission_id': data.permission_id})
        if not row:
            raise HTTPException(status_code=400, detail='permission has not founded')
        query = 'SELECT id FROM users WHERE id= :user_id'
        row = database.fetch_one(query=query, values={'user_id': data.user_id})
        if not row:
            raise HTTPException(status_code=400, detail='user has not founded')

