from fastapi import APIRouter

from api.department.schemas.department import CreateShtatDepartmentSchema
from api.department.services.department import DepartmentService


router = APIRouter()


@router.post('/department/',  tags=['department'])
async def create_department(data: CreateShtatDepartmentSchema):
    service_result = await DepartmentService().create_department(data=data)
    return {'status': 'success'}


@router.get('/department/list/',  tags=['department'])
async def create_department():
    service_result = await DepartmentService().department_list()
    return service_result


