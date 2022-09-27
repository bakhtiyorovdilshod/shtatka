from api.department.schemas.shtatka import ChangeShtatkaStatus
from fastapi import APIRouter, Request, Depends, HTTPException

from api.department.schemas.shtatka import ChangeShtatkaStatus
from api.user.schemas.user import UserDetailSchema
from api.user.services.auth import is_authenticated
from core.settings import database


class ShtatConfirmationStep:
    @staticmethod
    async def change_status(data: ChangeShtatkaStatus, user: UserDetailSchema = Depends(is_authenticated)):
        is_real_shtatka = await database.fetch_one(
            query='SELECT id FROM client_shtatkas WHERE id= :id',
            values={'id': data.client_shtatka_id}
        )
        if not is_real_shtatka:
            raise HTTPException(status_code=400, detail='shtatka does not exist')
        role = await database.fetch_one(
            query='SELECT name FROM user_roles WHERE id= :id',
            values={'id': user.role_id}
        )
        if role:
            raise HTTPException(status_code=400, detail='user role has not found')
        if role.name not in ['staff', 'head_staff']:
            raise HTTPException(status_code=400, detail='you do not have permission')
        shtatka = await database.fetch_one(
            query='SELECT shtatka_status FROM client_shtatkas WHERE id= :id',
            values={'id': data.client_shtatka_id}
        )
        if role.name == 'staff':
            if shtatka.shtatka_status != 'pending':
                raise HTTPException(status_code=400, detail='you do not have permission')
        elif role.name == 'head_staff':
            if shtatka.shtatka_status != 'checked':
                raise HTTPException(status_code=400, detail='you do not have permission')

        elif role.name == 'head_department_staff':
            if shtatka.shtatka_status != 'checked':
                raise HTTPException(status_code=400, detail='you do not have permission')


