from fastapi import APIRouter, Request, Depends

from api.user.schemas.user import UserDetailSchema
from api.user.services.auth import UserAuthenticationService, is_authenticated

from api.department.schemas.department import CreateShtatDepartmentSchema, UpdateShtatDepartmentSchema
from api.department.services.department import DepartmentService


router = APIRouter()


@router.post('/department/',  tags=['department'])
async def create_department(data: CreateShtatDepartmentSchema, user: UserDetailSchema = Depends(is_authenticated)):
    service_result = await DepartmentService().create_department(data=data)
    return {'status': 'success'}


@router.get('/department/list/',  tags=['department'])
async def create_department(page: int = 1, page_size: int = 2, request: Request = None, user: UserDetailSchema = Depends(is_authenticated)):
    service_result = await DepartmentService().all_for_pagination(page=page, page_size=page_size, request=request)
    return service_result


@router.get('/department/{id}/',  tags=['department'])
async def get_organization_detail(id: int):
    service_result = await DepartmentService().department_detail(department_id=id)
    return service_result


@router.put('/department/{id}/',  tags=['department'])
async def get_organization_detail(id: int, data: UpdateShtatDepartmentSchema):
    service_result = await DepartmentService().update_department(data=data, shtat_department_id=id)
    return service_result


