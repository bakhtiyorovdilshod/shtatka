from fastapi import APIRouter, Request, Depends

from api.department.schemas.settings import GivePermissionSchema
from api.department.services.settings import DepartmentSettingsService
from api.user.schemas.user import UserDetailSchema
from api.user.services.auth import  is_authenticated


router = APIRouter()


@router.post('/permission_change/',  tags=['permissions'])
async def permission_change(data: GivePermissionSchema, user: UserDetailSchema = Depends(is_authenticated)):
    service_result = await DepartmentSettingsService().give_permission(data=data)
    return {'status': 'success'}