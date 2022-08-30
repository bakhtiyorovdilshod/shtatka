from fastapi import APIRouter, Request
from typing import Optional

from api.user.schemas.user import UpdateOrganizationSchema, CreateRoleSchema
from api.user.services.user import UserService

router = APIRouter()


@router.get('/shtat/select_user/',  tags=['user'])
async def search_user(search: Optional[str] = None):
    return await UserService().search_user(name=search)


@router.get('/shtat/organization/',  tags=['user'])
async def organizations(page: int = 1, page_size: int = 10, request: Request = None):
    return await UserService().get_organizations(page=page, page_size=page_size, domain_name=request.url._url)


@router.get('/shtat/organization/{id}/',  tags=['user'])
async def get_organization_detail(id: int):
    return await UserService().get_detail_organization(organization_id=id)


@router.put('/shtat/organization/{id}/', tags=['user'])
async def edit_organization(id: int, data: UpdateOrganizationSchema):
    return await UserService().edit_organization(organization_id=id, data=data)


@router.get('/shtat/role/list/',  tags=['role'])
async def user_roles():
    return await UserService().user_role_list()


@router.post('/shtat/role/create/', tags=['role'])
async def role_create(data: CreateRoleSchema):
    role = await UserService().user_role_create(data=data)
    return {'status': 'success'}
