from typing import Union, Optional
import requests, json
from fastapi import HTTPException, Depends
from sqlalchemy import select
from passlib.hash import pbkdf2_sha256

from api.user.schemas.user import UpdateOrganizationSchema, CreateRoleSchema, UserCreateSchema, UserLoginSchema, \
    UserChangeStatus, UserPasswordCheck, UserDetailSchema, UserChangePassword
from api.user.services.auth import UserAuthenticationService, is_authenticated
from api.user.utils.page import fix_pagination
from api.user.utils.queryset import Queryset
from apps.user.models import UserRoleTable, UserTable, OrganizationTable
from core.settings import database


class UserService(Queryset):
    model = OrganizationTable

    @staticmethod
    async def search_user(name: Optional[str] = None):
        headers = {
            'content-type': 'application/json; charset=utf8'
        }
        url = f'https://hr.mf.uz/api/v1/shtat/select_user/?search={name}'
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            return response.json()
        return []

    @staticmethod
    async def get_organizations(domain_name: str, name: Optional[str] = None):
        headers = {
            'content-type': 'application/json; charset=utf8'
        }
        url = f'https://hr.mf.uz/api/v1/shtat/organization/?search={name}'
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            return response.json()
        return []
    @staticmethod
    async def get_shtat_organizations():
        query = 'SELECT * FROM shtat_organizations'
        organizations = await database.fetch_all(query=query, values={})


    @staticmethod
    async def get_detail_organization(organization_id: int):
        headers = {
            'content-type': 'application/json; charset=utf8'
        }
        url = f'https://hr.mf.uz/api/v1/shtat/organization/{organization_id}/'
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            return response.json()
        return []

    @staticmethod
    async def edit_organization(organization_id: int, data=UpdateOrganizationSchema):
        headers = {
            'content-type': 'application/json; charset=utf8'
        }
        url = f'https://hr.mf.uz/api/v1/shtat/organization/{organization_id}/'
        json_data = {
            'chapter_code': data.chapter_code,
            'department_code': data.department_code,
            'small_department_code': data.small_department_code
        }
        json_data = json.dumps(json_data)
        response = requests.put(url=url, headers=headers, data=json_data, verify=False)
        return response.status_code

    @staticmethod
    async def user_role_list():
        data = []
        roles = select([UserRoleTable])
        results = await database.fetch_all(roles)
        for result in results:
            data.append({
                'id': result.id,
                'name': result.name
            })
        return data

    @staticmethod
    async def user_role_create(data: CreateRoleSchema):
        async with database.transaction():
            query = 'SELECT name FROM user_roles WHERE name = :name '
            result = await database.fetch_one(query=query, values={'name': data.name})
            if result:
                raise HTTPException(status_code=400, detail='role has already existed')
            role = UserRoleTable.insert().values(
                name=data.name
            )
            role_id = await database.execute(role)
            return role_id

    @staticmethod
    async def create_user(data: UserCreateSchema):
        async with database.transaction():
            query = 'SELECT username FROM users WHERE username = :username or pinfl = :pinfl'
            has_user = await database.fetch_one(query=query, values={'username': data.username, 'pinfl': data.pinfl})
            if has_user:
                raise HTTPException(status_code=400, detail='user has already existed')

            role_query = 'SELECT id FROM user_roles WHERE id = :role_id'
            role_id = await database.fetch_one(query=role_query, values={'role_id': data.role_id})
            if not role_id:
                raise HTTPException(status_code=404, detail='role_id has not found')

            user = UserTable.insert().values(
                full_name=data.full_name,
                username=data.username,
                pinfl=data.pinfl,
                password=pbkdf2_sha256.hash(data.password),
                role_id=data.role_id,
                is_active=True
            )
            user_id = await database.execute(user)
            access_token = UserAuthenticationService().create_access_token(user_id)
            return {'status': 'success', 'access_token': access_token, 'user_id': user_id}

    @staticmethod
    async def login(data: UserLoginSchema):
        login_query = 'SELECT users.username, users.id,users.password, user_roles.name, users.is_active ' \
                      'FROM users INNER JOIN user_roles ON users.role_id=user_roles.id WHERE username = :username'
        user = await database.fetch_one(query=login_query, values={'username': data.username})

        if not user:
            raise HTTPException(status_code=400, detail='username is in incorrect')
        if not pbkdf2_sha256.verify(data.password, user.password):
            raise HTTPException(status_code=400, detail='password is in incorrect')

        if not user.is_active:
            raise HTTPException(status_code=400, detail='user is not active')

        access_token = UserAuthenticationService().create_access_token(user.id)
        return {'status': 'success', 'access_token': access_token, 'user_id': user.id, 'role': user.name}

    @staticmethod
    async def shtat_users():
        data = []
        query = 'SELECT users.id, users.full_name, user_roles.name, users.is_active, users.username FROM users INNER JOIN user_roles ON users.role_id = user_roles.id'
        users = await database.fetch_all(query=query, values={})
        for user in users:
            department = None
            query = 'SELECT * FROM shtat_department_users INNER JOIN shtat_departments ON shtat_department_users.shtat_department_id=shtat_departments.id WHERE shtat_department_users.user_id= :user_id'
            department_query = await database.fetch_one(query=query, values={'user_id': user.id})
            if department_query:
                department = {
                    'id': department_query.id,
                    'name': department_query.name,
                    'code': department_query.code
                }
            data.append({
                'id': user.id,
                'full_name': user.full_name,
                'role': user.name,
                'is_active': user.is_active,
                'username': user.username,
                'department': department
            })
        return data

    @staticmethod
    async def change_status(data: UserChangeStatus):
        real_user = await database.fetch_one(
            query='SELECT id FROM users WHERE id= :user_id',
            values={'user_id': data.user_id}
        )
        if not real_user:
            raise HTTPException(status_code=400, detail="user is not found")
        await database.execute(
            query='UPDATE users SET is_active= :is_active WHERE id= :user_id;',
            values={'user_id': data.user_id, 'is_active': data.is_active}
        )
        return {'status': 'success'}

    @staticmethod
    async def check_password(data: UserPasswordCheck, user: UserDetailSchema = Depends(is_authenticated)):
        user = await database.fetch_one(
            query='SELECT password FROM users WHERE id= :user_id',
            values={'user_id': user.id}
        )
        if not pbkdf2_sha256.verify(data.password, user.password):
            raise HTTPException(status_code=400, detail={'message': 'Parol xato kiritildi'})
        return {'status': 'success'}

    @staticmethod
    async def change_password(data: UserChangePassword, user: UserDetailSchema = Depends(is_authenticated)):
        user = await database.execute(
            query='UPDATE users set password= :new_password WHERE id= :user_id',
            values={'user_id': user.id, 'new_password': pbkdf2_sha256.hash(data.password)}
        )
        return {'status': 'success'}








