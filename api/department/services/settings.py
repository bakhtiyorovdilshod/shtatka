from fastapi import HTTPException

from api.department.schemas.settings import GivePermissionSchema
from api.user.utils.queryset import Queryset
from core.settings import database


class DepartmentSettingsService:

    @staticmethod
    async def give_permission(data: GivePermissionSchema):
        query = 'SELECT id FROM users WHERE id= :user_id'
        user_row = database.fetch_one(query=query, values={'user_id': data.user_id})
        if not user_row:
            raise HTTPException(status_code=400, detail='user has not founded')
        insert_query = None
        values = list()
        for permission in data.permissions:
            insert_query = 'INSERT INTO UserPermissionTable(user_id, permission_id) VALUES (:user_id, :permission_id)'
            permission_row = database.fetch_one(query=query, values={'permission_id': permission.permission_id})
            if not permission_row:
                raise HTTPException(status_code=400, detail='permission has not founded')
            values.append({
                'user_id': user_row.id,
                'permission_id': permission.permission_id
            })
        if insert_query:
            await database.execute_many(query=query, values=values)
        return True





