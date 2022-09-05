from fastapi import HTTPException
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from api.department.schemas.department import CreateShtatDepartmentSchema, UpdateShtatDepartmentSchema
from api.user.utils.queryset import Queryset
from apps.user.models import ShtatDepartmentTable, ShtatDepartmentUser, UserTable, OrganizationTable, \
    ShtatDepartmentOrganizationTable
from core.settings import database


class DepartmentService(Queryset):
    model = ShtatDepartmentTable

    @staticmethod
    async def create_department(data: CreateShtatDepartmentSchema):
        async with database.transaction():
            users = data.users
            organizations = data.organizations
            query = 'SELECT code FROM shtat_departments WHERE code = :code '
            result = await database.fetch_one(query=query, values={'code': data.code})
            if result:
                raise HTTPException(status_code=400, detail='shtat department has already existed')
            shtat_department = ShtatDepartmentTable.insert().values(
               name=data.name,
               code=data.code
            )
            shtat_department_id = await database.execute(shtat_department)
            for user_item in users:
                is_exist_user = 'SELECT id, username, pinfl FROM users WHERE username= :username or pinfl= :pinfl'
                result = await database.fetch_one(query=is_exist_user, values={'username': user_item.username, 'pinfl': user_item.pinfl})
                if not result:
                    user = UserTable.insert().values(
                        full_name=user_item.full_name,
                        pinfl=user_item.pinfl,
                        role_id=user_item.role_id,
                        username=user_item.username,
                        password=pbkdf2_sha256.hash('test_password'),
                    )
                    user_id = await database.execute(user)
                else:
                    user_id = result.id
                shtat_user_val_query = 'SELECT user_id FROM  shtat_department_users WHERE user_id= :user_id'
                result = await database.fetch_one(query=shtat_user_val_query, values={'user_id': user_id})
                if result:
                    raise HTTPException(status_code=400, detail='user has already been connected other department')

                shtat_department_user = ShtatDepartmentUser.insert().values(
                    user_id=user_id,
                    shtat_department_id=shtat_department_id
                )
                await database.execute(shtat_department_user)
            for organization_item in organizations:
                organization_val_query = 'SELECT organization_tin, id FROM shtat_organizations WHERE organization_tin= :organization_tin'
                result = await database.fetch_one(query=organization_val_query, values={'organization_tin': organization_item.organization_tin})
                if not result:
                    organization = OrganizationTable.insert().values(
                        organization_tin=organization_item.organization_tin,
                        name=organization_item.name
                    )
                    organization_id = await database.execute(organization)
                else:
                    organization_id = result.id
                shtat_department_organization = ShtatDepartmentOrganizationTable.insert().values(
                    shtat_department_id=shtat_department_id,
                    organization_id=organization_id
                )
                await database.execute(shtat_department_organization)

    @staticmethod
    async def department_list():
        data = []
        query = 'SELECT id, name, code FROM shtat_departments'
        rows = await database.fetch_all(query=query)
        for row in rows:
            data.append({
                'id': row.id,
                'name': row.name,
                'code': row.code
            })
        return data

    @staticmethod
    async def department_detail(department_id: int):
        data = []
        query = 'SELECT name, code, id FROM shtat_departments WHERE id= :department_id'
        shtat_department = await database.fetch_one(query=query, values={'department_id': department_id})
        user_list = []
        organization_list = []
        user_query = 'SELECT users.id, users.role_id, users.full_name FROM shtat_department_users INNER JOIN users ' \
                     'ON users.id= shtat_department_users.user_id WHERE shtat_department_users.shtat_department_id= :shtat_department_id'
        users = await database.fetch_all(query=user_query, values={'shtat_department_id': shtat_department.id})
        for user in users:
            user_list.append({
                'id': user.id,
                'full_name': user.full_name,
                'role': user.role_id
            })
        organ_query = 'SELECT * ' \
                      'FROM shtat_department_organizations INNER JOIN shtat_organizations ' \
                      'ON shtat_organizations.id=shtat_department_organizations.organization_id ' \
                      'WHERE shtat_department_organizations.shtat_department_id= :shtat_department_id'
        organizations = await database.fetch_all(query=organ_query, values={'shtat_department_id': shtat_department.id})
        for organization in organizations:
            organization_list.append({
                'name': organization.name,
                'organization_tin': organization.organization_tin
            })
        data.append({
            'id': shtat_department.id,
            'name': shtat_department.name,
            'code': shtat_department.code,
            'users': user_list,
            'organizations': organization_list
        })
        return data

    @staticmethod
    async def update_department(data: UpdateShtatDepartmentSchema, shtat_department_id: int):
        async with database.transaction():
            query = 'SELECT id, code FROM shtat_departments WHERE code = :code '
            result = await database.fetch_one(query=query, values={'code': data.code})
            if result:
                if result.id != shtat_department_id:
                    raise HTTPException(status_code=400, detail='shtat department has already existed')
            query = 'UPDATE shtat_departments SET name= :name, code= :code WHERE id= :shtat_department_id'
            await database.execute(query=query, values={'name': data.name, 'code': data.code, 'shtat_department_id': shtat_department_id})
            delete_user_query = 'DELETE FROM shtat_department_users WHERE shtat_department_id= :shtat_department_id'
            await database.execute(query=delete_user_query, values={'shtat_department_id': shtat_department_id})
            delete_organization = 'DELETE FROM shtat_department_organizations WHERE shtat_department_id= :shtat_department_id'
            await database.execute(query=delete_organization, values={'shtat_department_id': shtat_department_id})
            users = data.users
            organizations = data.organizations
            for user_item in users:
                is_exist_user = 'SELECT id, username, pinfl FROM users WHERE username= :username or pinfl= :pinfl'
                result = await database.fetch_one(query=is_exist_user, values={'username': user_item.username, 'pinfl': user_item.pinfl})
                if not result:
                    user = UserTable.insert().values(
                        full_name=user_item.full_name,
                        pinfl=user_item.pinfl,
                        role_id=user_item.role_id,
                        username=user_item.username,
                        password=pbkdf2_sha256.hash('test_password'),
                    )
                    user_id = await database.execute(user)
                else:
                    user_id = result.id
                shtat_user_val_query = 'SELECT user_id FROM  shtat_department_users WHERE user_id= :user_id'
                result = await database.fetch_one(query=shtat_user_val_query, values={'user_id': user_id})
                if result:
                    raise HTTPException(status_code=400, detail='user has already been connected other department')

                shtat_department_user = ShtatDepartmentUser.insert().values(
                    user_id=user_id,
                    shtat_department_id=shtat_department_id
                )
                await database.execute(shtat_department_user)
            for organization_item in organizations:
                organization_val_query = 'SELECT organization_tin, id FROM shtat_organizations WHERE organization_tin= :organization_tin'
                result = await database.fetch_one(query=organization_val_query, values={'organization_tin': organization_item.organization_tin})
                if not result:
                    organization = OrganizationTable.insert().values(
                        organization_tin=organization_item.organization_tin,
                        name=organization_item.name
                    )
                    organization_id = await database.execute(organization)
                else:
                    organization_id = result.id
                shtat_department_organization = ShtatDepartmentOrganizationTable.insert().values(
                    shtat_department_id=shtat_department_id,
                    organization_id=organization_id
                )
                await database.execute(shtat_department_organization)
        return {'success'}





