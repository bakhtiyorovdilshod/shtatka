from fastapi import APIRouter, Request, Depends

from api.department.schemas.settings import GivePermissionSchema, CreatePermissionSchema
from api.department.services.settings import DepartmentSettingsService
from api.user.schemas.user import UserDetailSchema
from api.user.services.auth import  is_authenticated


router = APIRouter()


@router.post('/permission_change/',  tags=['permissions'])
async def permission_change(data: GivePermissionSchema, user: UserDetailSchema = Depends(is_authenticated)):
    await DepartmentSettingsService().give_permission(data=data)
    return {'status': 'success'}


@router.post('/create_permission/',  tags=['permissions'])
async def create_permission(data: CreatePermissionSchema, user: UserDetailSchema = Depends(is_authenticated)):
    await DepartmentSettingsService().create_permission(data=data)
    return {'status': 'success'}


@router.post('/permissions/',  tags=['permissions'])
async def permissions(user: UserDetailSchema = Depends(is_authenticated)):
    return await DepartmentSettingsService().permissions()