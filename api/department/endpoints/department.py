from fastapi import APIRouter, Request, Depends

from api.department.utils.excel import xls_response
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
async def department_list(page: int = 1, page_size: int = 5, request: Request = None, user: UserDetailSchema = Depends(is_authenticated)):
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


@router.delete('/department/{id}/', tags=['department'])
async def delete_department(id: int):
    status = await DepartmentService().delete_department(shtat_department_id=id)
    return status


@router.get('/department/list/users/',  tags=['department_users'])
async def department_users(user: UserDetailSchema = Depends(is_authenticated)):
    result = await DepartmentService().department_users(user=user)
    return result


@router.get('/departments/sent_shtatka/',  tags=['sent_shtatka'])
async def department_shtatka(page: int = 1, page_size: int = 2, user: UserDetailSchema = Depends(is_authenticated), request: Request = None):
    result = await DepartmentService().client_shtatka_list(page=page, page_size=page_size, user=user, request=request)
    return result


@router.get('/departments/sent_shtatka/{client_shtatka_id}/',  tags=['sent_shtatka'])
async def department_users(client_shtatka_id: int, page: int = 1, page_size: int = 1,
                           user: UserDetailSchema = Depends(is_authenticated),
                           request: Request = None, region_id: int = None, district_id: int = None):
    result = await DepartmentService().client_shtatka_detail(client_shtatka_id=client_shtatka_id, user=user, page=page,
                                                             page_size=page_size, request=request,
                                                             region_id=region_id, district_id=district_id)
    return result


@router.get('/departments/sent_shtatka/{client_shtatka_id}/regions/',  tags=['sent_shtatka'])
async def client_shtatka_regions(client_shtatka_id: int):
    result = await DepartmentService().client_shtatka_regions(client_shtatka_id=client_shtatka_id)
    return result


@router.get('/departments/sent_shtatka/region/{region_id}/districts/',  tags=['sent_shtatka'])
async def client_shtatka_regions(region_id: int):
    result = await DepartmentService().client_shtatka_region_districts(region_id=region_id)
    return result


@router.get('/departments/sent_shtatka/{child_shtatka_id}/get_excel/',  tags=['sent_shtatka'])
async def department_users(child_shtatka_id: int, user: UserDetailSchema = Depends(is_authenticated)):
    result = await DepartmentService().convert_execl(child_shtatka_id=child_shtatka_id)
    return xls_response(result, 'shtatka.xlsx')





