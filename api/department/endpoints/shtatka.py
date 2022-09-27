from fastapi import APIRouter, Request, Depends

from api.department.schemas.shtatka import ChangeShtatkaStatus
from api.department.utils.excel import xls_response
from api.user.schemas.user import UserDetailSchema
from api.user.services.auth import UserAuthenticationService, is_authenticated

from api.department.schemas.department import CreateShtatDepartmentSchema, UpdateShtatDepartmentSchema
from api.department.services.department import DepartmentService


router = APIRouter()


@router.post('/change_status/',  tags=['department'])
async def change_shtatka_status(data: ChangeShtatkaStatus, user: UserDetailSchema = Depends(is_authenticated)):
    service_result = await DepartmentService().create_department(data=data)
    return {'status': 'success'}