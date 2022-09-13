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
async def department_list(page: int = 1, page_size: int = 2, request: Request = None, user: UserDetailSchema = Depends(is_authenticated)):
    service_result = await DepartmentService().all_for_pagination(page=page, page_size=page_size, request=request)
    return service_result


@router.get('/department/{id}/',  tags=['department'])
async def get_organization_detail(id: int):
    service_result = await DepartmentService().department_detail(department_id=id)
    return service_result


@router.put('/department/{id}/',  tags=['department'])
async def edit_department(id: int, data: UpdateShtatDepartmentSchema):
    service_result = await DepartmentService().update_department(data=data, shtat_department_id=id)
    return service_result


@router.get('/department/{id}/list/users/',  tags=['department_users'])
async def department_users(id: int, user: UserDetailSchema = Depends(is_authenticated)):
    result = await DepartmentService().department_users(department_id=id)
    return result


@router.get('/department/{department_id}/sent_shtatka/',  tags=['sent_shtatka'])
async def department_users(department_id: int, user: UserDetailSchema = Depends(is_authenticated)):
    result = await DepartmentService().client_shtatka_list(shtat_department_id=department_id)
    return result


@router.get('/department/{department_id}/sent_shtatka/{client_shtatka_id}/',  tags=['sent_shtatka'])
async def department_users(department_id: int, client_shtatka_id, user: UserDetailSchema = Depends(is_authenticated)):
    result = await DepartmentService().client_shtatka_detail(shtat_department_id=department_id, client_shtatka_id=client_shtatka_id)
    return result


