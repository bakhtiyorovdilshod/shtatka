from fastapi import APIRouter

from api.department.schemas.department import CreateShtatDepartmentSchema
from api.department.services.department import DepartmentService


router = APIRouter()


@router.post('/department/',  tags=['department'])
async def create_department(data: CreateShtatDepartmentSchema):
    return await DepartmentService().create_department(data=data)
