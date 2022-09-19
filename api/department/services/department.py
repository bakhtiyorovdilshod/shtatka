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
                if organization_item.type not in ['with_self', 'with_budget']:
                    raise HTTPException(status_code=400, detail='type has not been matched')
                query = 'SELECT shtat_department_organizations.id FROM shtat_department_organizations ' \
                        'INNER JOIN shtat_organizations ON ' \
                        'shtat_department_organizations.organization_id=shtat_organizations.id ' \
                        'WHERE type= :type and shtat_organizations.organization_tin= :organization_tin'
                organization_other_department = await database.fetch_one(
                    query=query,
                    values={
                        'type': organization_item.type,
                        'organization_tin': organization_item.organization_tin
                    }
                )
                if organization_other_department:
                    raise HTTPException(status_code=400, detail='organization has already fixed to another department')

                organization_val_query = 'SELECT organization_tin, id FROM shtat_organizations ' \
                                         'WHERE organization_tin= :organization_tin'
                result = await database.fetch_one(
                    query=organization_val_query,
                    values={'organization_tin': organization_item.organization_tin}
                )
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
                    organization_id=organization_id,
                    type=organization_item.type
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
        query = 'SELECT name, code, id FROM shtat_departments WHERE id= :department_id'
        shtat_department = await database.fetch_one(query=query, values={'department_id': department_id})
        user_list = []
        organization_list = []
        user_query = 'SELECT * FROM shtat_department_users INNER JOIN users ' \
                     'ON users.id= shtat_department_users.user_id WHERE shtat_department_users.shtat_department_id= :shtat_department_id'
        users = await database.fetch_all(query=user_query, values={'shtat_department_id': shtat_department.id})
        for user in users:
            user_list.append({
                'id': user.id,
                'full_name': user.full_name,
                'role_id': user.role_id,
                'username': user.username,
                'pinfl': user.pinfl
            })
        organ_query = 'SELECT * ' \
                      'FROM shtat_department_organizations INNER JOIN shtat_organizations ' \
                      'ON shtat_organizations.id=shtat_department_organizations.organization_id ' \
                      'WHERE shtat_department_organizations.shtat_department_id= :shtat_department_id'
        organizations = await database.fetch_all(query=organ_query, values={'shtat_department_id': shtat_department.id})
        for organization in organizations:
            organization_list.append({
                'name': organization.name,
                'organization_tin': organization.organization_tin,
                'type': organization.type
            })
        data = {
            'id': shtat_department.id,
            'name': shtat_department.name,
            'code': shtat_department.code,
            'users': user_list,
            'organizations': organization_list
        }
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
                    organization_id=organization_id,
                    type=organization_item.type
                )
                await database.execute(shtat_department_organization)
        return {'success'}

    @staticmethod
    async def delete_department(shtat_department_id: int):
        delete_department_query = 'DELETE FROM shtat_departments WHERE id= :shtat_department_id'
        await database.execute(query=delete_department_query, values={'shtat_department_id': shtat_department_id})
        shtat_department_users = await database.fetch_all(
            query='SELECT * FROM shtat_department_users INNER JOIN users '
                  'ON users.id= shtat_department_users.user_id WHERE shtat_department_id= :shtat_department_id',
            values={'shtat_department_id': shtat_department_id}
        )
        for shtat_department_user in shtat_department_users:
            await database.execute(
                query='DELETE FROM users WHERE id= : id',
                values={'id': shtat_department_user.user_id}
            )
        delete_user_query = 'DELETE FROM shtat_department_users WHERE shtat_department_id= :shtat_department_id'
        await database.execute(query=delete_user_query, values={'shtat_department_id': shtat_department_id})
        delete_organization = 'DELETE FROM shtat_department_organizations WHERE shtat_department_id= :shtat_department_id'
        await database.execute(query=delete_organization, values={'shtat_department_id': shtat_department_id})
        return {'status': 'success'}

    @staticmethod
    async def department_users(department_id: int):
        data = []
        query = 'SELECT users.id, users.full_name FROM shtat_department_users INNER JOIN users ' \
                'ON shtat_department_users.user_id=users.id WHERE shtat_department_id= :department_id'
        users = await database.fetch_all(query=query, values={'department_id': department_id})
        for user in users:
            user_permissions = []
            query = 'SELECT permissions.id, permissions.name FROM user_permissions INNER JOIN permissions ON user_permissions.permission_id=permissions.id WHERE user_id= :user_id'
            permissions = await database.fetch_all(query=query, values={'user_id': user.id})
            for permission in permissions:
                user_permissions.append({
                    'id': permission.id,
                    'name': permission.name
                })
            data.append({
                'id': user.id,
                'full_name': user.full_name,
                'permissions': user_permissions
            })
        return data

    @staticmethod
    async def client_shtatka_list(shtat_department_id: int):
        data = []
        shtatka_query = 'SELECT * FROM client_shtatkas INNER JOIN shtat_organizations ' \
                        'ON client_shtatkas.parent_id=shtat_organizations.id ' \
                        'WHERE parent_id in (' \
                        'SELECT organization_id FROM shtat_department_organizations ' \
                        'WHERE shtat_department_id= :shtat_department_id )'
        shtatkas = await database.fetch_all(query=shtatka_query, values={'shtat_department_id': shtat_department_id})
        for shtatka in shtatkas:
            data.append({
                'id': shtatka.id,
                'status': shtatka.status,
                'organization_name': shtatka.name,
                'organization_tin': shtatka.organization_tin,
            })
        return data

    @staticmethod
    async def client_shtatka_detail(shtat_department_id: int, client_shtatka_id: int):
        data = []
        shtatka_query = 'SELECT * FROM client_shtatkas INNER JOIN shtat_organizations ' \
                        'ON client_shtatkas.parent_id=shtat_organizations.id ' \
                        'WHERE client_shtatkas.id= :client_shtatka_id and parent_id in (' \
                        'SELECT organization_id FROM shtat_department_organizations ' \
                        'WHERE shtat_department_id= :shtat_department_id )'
        shtatka = await database.fetch_one(
            query=shtatka_query,
            values={
                'shtat_department_id': shtat_department_id,
                'client_shtatka_id': int(client_shtatka_id)
            })
        if shtatka:
            documents = []
            query = 'SELECT * FROM organization_children WHERE client_shtatka_id= :client_shtatka_id'
            organization_children = await database.fetch_all(query=query, values={'client_shtatka_id': shtatka.id})
            for child in organization_children:
                department_list = []
                department_query = 'SELECT * FROM client_departments WHERE child_id= :child_id'
                departments = await database.fetch_all(query=department_query, values={'child_id': child.id})
                for department in departments:
                    position_list = []
                    positions = await database.fetch_all(query='SELECT * FROM client_department_positions '
                                                               'WHERE client_department_id= :client_department_id',
                                                         values={
                                                             'client_department_id': department.id
                                                         })
                    for position in positions:
                        position_list.append({
                            'name': position.name,
                            'base_salary': position.base_salary,
                            'count': position.count,
                            'bonus_salary': position.bonus_salary,
                            'minimal_salary': position.minimal_salary,
                            'other_bonus_salary': position.other_bonus_salary,
                            'razryad_coefficient': position.razryad_coefficient,
                            'razryad_value': position.razryad_value,
                            'razryad_subtract': position.razryad_subtract,
                            'right_coefficient': position.right_coefficient
                        })
                    department_list.append({
                        'name': department.name,
                        'positions': position_list,
                        'total_count': department.total_count,
                        'total_minimal_salary': department.total_minimal_salary,
                        'total_bonus_salary': department.total_bonus_salary,
                        'total_base_salary': department.total_base_salary,

                    })
                documents.append({
                    'name': child.child_name,
                    'address': child.address,
                    'chapter_code': child.chapter_code,
                    'department_code': child.department_code,
                    'small_department_code': child.small_department_code,
                    'is_main': child.is_main,
                    'departments': department_list
                })
            data.append({
                'id': shtatka.id,
                'status': shtatka.status,
                'organization_name': shtatka.name,
                'organization_tin': shtatka.organization_tin,
                'documents': documents
            })
            return data
        else:
            return {}








