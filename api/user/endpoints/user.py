import databases
from fastapi import APIRouter, Request
from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from api.user.schemas.user import UpdateOrganizationSchema, CreateRoleSchema, UserCreateSchema, UserLoginSchema, \
    UserDetailSchema
from api.user.services.auth import UserAuthenticationService, is_authenticated
from api.user.services.user import UserService
from fastapi import Depends, HTTPException

from core.settings import database

router = APIRouter()


@router.post("/token/", tags=['token'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await database.fetch_one(query='SELECT id, password FROM users WHERE username = :username', values={'username': form_data.username})
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not pbkdf2_sha256.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = UserAuthenticationService().create_access_token(user.id)
    return {'status': 'success', 'access_token': access_token, 'user_id': user.id}


@router.get('/shtat/select_user/',  tags=['user'])
async def search_user(search: Optional[str] = None, user: UserDetailSchema = Depends(is_authenticated)):
    return await UserService().search_user(name=search)


@router.get('/shtat/organization/',  tags=['user'])
async def organizations(page: int = 1, page_size: int = 10, request: Request = None, user: UserDetailSchema = Depends(is_authenticated)):
    return await UserService().get_organizations(page=page, page_size=page_size, domain_name=request.url._url)


@router.get('/shtat/organization/{id}/',  tags=['user'])
async def get_organization_detail(id: int, user: UserDetailSchema = Depends(is_authenticated)):
    return await UserService().get_detail_organization(organization_id=id)


@router.put('/shtat/organization/{id}/', tags=['user'])
async def edit_organization(id: int, data: UpdateOrganizationSchema, user: UserDetailSchema = Depends(is_authenticated)):
    return await UserService().edit_organization(organization_id=id, data=data)


@router.get('/shtat/role/list/',  tags=['role'])
async def user_roles(user: UserDetailSchema = Depends(is_authenticated)):
    return await UserService().user_role_list()


@router.post('/shtat/role/create/', tags=['role'])
async def role_create(data: CreateRoleSchema, user: UserDetailSchema = Depends(is_authenticated)):
    role = await UserService().user_role_create(data=data)
    return {'status': 'success'}


@router.post('/shtat/user/register/', tags=['user'])
async def create_user(data: UserCreateSchema):
    result = await UserService().create_user(data=data)
    return result


@router.post('/shtat/user/login/', tags=['user'])
async def login_user(data: UserLoginSchema):
    result = await UserService().login(data=data)
    return result


@router.get('/shtat/users/', tags=['user'])
async def login_user():
    result = await UserService().shtat_users()
    return result
