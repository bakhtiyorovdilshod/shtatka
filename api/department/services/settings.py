from fastapi import HTTPException

from api.department.schemas.settings import GivePermissionSchema, CreatePermissionSchema
from api.user.utils.queryset import Queryset
from apps.user.models import PermissionTable
from core.settings import database


class DepartmentSettingsService:

    @staticmethod
    async def give_permission(data: GivePermissionSchema):
        query = 'SELECT id FROM users WHERE id= :user_id'
        user_row = await database.fetch_one(query=query, values={'user_id': data.user_id})
        if not user_row:
            raise HTTPException(status_code=400, detail='user has not founded')
        insert_query = None
        values = list()
        for permission in data.permissions:
            insert_query = 'INSERT OR UPDATE user_permissions.Records (user_id, permission_id) VALUES (:user_id, :permission_id)'
            permission_query = 'SELECT id FROM permissions WHERE id= :permission_id'
            permission_row = await database.fetch_one(query=permission_query, values={'permission_id': permission.permission_id})
            if not permission_row:
                raise HTTPException(status_code=400, detail='permission has not founded')
            values.append({
                'user_id': user_row.id,
                'permission_id': permission.permission_id
            })
        if insert_query:
            await database.execute_many(query=insert_query, values=values)
        return True

    @staticmethod
    async def create_permission(data: CreatePermissionSchema):
        async with database.transaction():
            query = 'SELECT id, name FROM permissions WHERE name= :name'
            row = await database.fetch_one(query=query, values={'name': data.name})
            if row:
                raise HTTPException(status_code=400, detail='permission has already existed')
            permission = PermissionTable.insert().values(
                name=data.name
            )
            permission_id = await database.execute(permission)
            return True

    @staticmethod
    async def permissions():
        data = []
        query = 'SELECT id, name FROM permissions'
        permissions = await database.fetch_all(query=query, values={})
        for permission in permissions:
            data.append({
                'id': permission.id,
                'name': permission.name
            })
        return data






