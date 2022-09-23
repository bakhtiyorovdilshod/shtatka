from io import BytesIO

from fastapi import HTTPException, Depends
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from xlsxwriter import Workbook

from api.department.schemas.department import CreateShtatDepartmentSchema, UpdateShtatDepartmentSchema
from api.department.utils.page import get_next_page, get_count, get_prev_page, get_page
from api.user.schemas.user import UserDetailSchema
from api.user.services.auth import is_authenticated
from api.user.utils.queryset import Queryset
from apps.user.models import ShtatDepartmentTable, ShtatDepartmentUser, UserTable, OrganizationTable, \
    ShtatDepartmentOrganizationTable, ClientShtatkaTable
from core.settings import database
from fastapi import Request
import locale


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
                        is_active=True
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
                'id': organization.organization_id,
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
                        is_active=True
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
        shtat_department_users = await database.fetch_all(
            query='SELECT * FROM shtat_department_users  WHERE shtat_department_id= :shtat_department_id',
            values={'shtat_department_id': shtat_department_id}
        )
        for shtat_department_user in shtat_department_users:
            await database.execute(
                query='DELETE FROM users WHERE id= :id',
                values={'id': shtat_department_user.user_id}
            )
        await database.execute(query=delete_department_query, values={'shtat_department_id': shtat_department_id})
        delete_user_query = 'DELETE FROM shtat_department_users WHERE shtat_department_id= :shtat_department_id'
        await database.execute(query=delete_user_query, values={'shtat_department_id': shtat_department_id})
        delete_organization = 'DELETE FROM shtat_department_organizations WHERE shtat_department_id= :shtat_department_id'
        await database.execute(query=delete_organization, values={'shtat_department_id': shtat_department_id})
        return {'status': 'success'}

    @staticmethod
    async def department_users(user: UserDetailSchema = Depends(is_authenticated)):
        data = []
        query = 'SELECT users.id, users.full_name FROM shtat_department_users INNER JOIN users ' \
                'ON shtat_department_users.user_id=users.id WHERE user_id= :user_id'
        users = await database.fetch_all(query=query, values={'user_id': user.id})
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
    async def client_shtatka_list(page: int, page_size: int, user: UserDetailSchema = Depends(is_authenticated),  request: Request = None):
        domain_name = list(request.url._url.split('?')[0])
        domain_name.insert(4, 's')
        domain_name = ''.join(domain_name)
        results = []
        query = 'SELECT shtat_department_id FROM shtat_department_users WHERE user_id= :user_id'
        shtat_department = await database.fetch_one(query=query, values={'user_id': user.id})
        if shtat_department:
            shtat_department_id = shtat_department.shtat_department_id
            shtatka_query = 'SELECT  cl.id, cl.status,shto.name, shto.organization_tin ' \
                            'FROM client_shtatkas as cl INNER JOIN shtat_organizations as shto ' \
                            'ON cl.parent_id=shto.id ' \
                            'WHERE parent_id in (' \
                            'SELECT organization_id FROM shtat_department_organizations ' \
                            'WHERE shtat_department_id= :shtat_department_id) ORDER BY cl.id ' \
                            'LIMIT :page_size OFFSET :page; '
            page = get_page(page=page)
            shtatkas = await database.fetch_all(
                query=shtatka_query,
                values=
                {
                    'shtat_department_id': shtat_department_id,
                    'page_size': page_size,
                    'page': page
                })
            total_count = await get_count(ClientShtatkaTable)
            next_page = get_next_page(page=page+1, page_size=page_size, count=total_count, domain_name=domain_name)
            previous_page = get_prev_page(page=page+1, page_size=page_size, domain_name=domain_name)
            for shtatka in shtatkas:
                results.append({
                    'id': shtatka.id,
                    'status': shtatka.status,
                    'organization_name': shtatka.name,
                    'organization_tin': shtatka.organization_tin,
                })
            return dict(next=next_page, previous=previous_page, count=total_count, results=results)
        return []


    @staticmethod
    async def client_shtatka_detail(page: int, page_size: int, client_shtatka_id: int, user: UserDetailSchema = Depends(is_authenticated), request: Request = None):
        domain_name = list(request.url._url.split('?')[0])
        domain_name.insert(4, 's')
        domain_name = ''.join(domain_name)
        page = get_page(page)
        query = 'SELECT shtat_department_id FROM shtat_department_users WHERE user_id= :user_id'
        shtat_department = await database.fetch_one(query=query, values={'user_id': user.id})
        if shtat_department:
            shtatka_query = 'SELECT cl.id, cl.status,shto.name, shto.organization_tin, cl.parent_id ' \
                            'FROM client_shtatkas as cl INNER JOIN shtat_organizations as shto ' \
                            'ON cl.parent_id=shto.id ' \
                            'WHERE cl.id= :client_shtatka_id and ' \
                            'parent_id in (SELECT organization_id FROM shtat_department_organizations ' \
                            'WHERE shtat_department_id= :shtat_department_id)'
            shtatka = await database.fetch_one(
                query=shtatka_query,
                values={
                    'client_shtatka_id': int(client_shtatka_id),
                    'shtat_department_id': shtat_department.shtat_department_id
                })
            if shtatka:
                documents = []
                query = 'SELECT * FROM organization_children WHERE client_shtatka_id= :client_shtatka_id ORDER BY id ' \
                        'LIMIT :page_size OFFSET :page; '
                organization_children = await database.fetch_all(
                    query=query, values=
                    {
                        'client_shtatka_id': shtatka.id,
                        'page_size': page_size,
                        'page': page
                    })
                for child in organization_children:
                    department_list = []
                    department_query = 'SELECT * FROM client_departments WHERE child_id= :child_id'
                    departments = await database.fetch_all(query=department_query, values={'child_id': child.id})
                    for department in departments:
                        position_list = []
                        positions = await database.fetch_all(query='SELECT cdp.id, cdp.name, cdp.base_salary, cdp.position_count, '
                                                                   'cdp.bonus_salary,cdp.minimal_salary,'
                                                                   'cdp.other_bonus_salary, cdp.razryad_coefficient,'
                                                                   'cdp.razryad_value, cdp.razryad_subtract,'
                                                                   'cdp.right_coefficient '
                                                                   'FROM client_department_positions as cdp '
                                                                   'WHERE client_department_id= :client_department_id',
                                                             values={
                                                                 'client_department_id': department.id
                                                             })
                        for position in positions:
                            position_list.append({
                                'id': position.id,
                                'name': position.name,
                                'base_salary': position.base_salary,
                                'position_count': position.position_count,
                                'bonus_salary': position.bonus_salary,
                                'minimal_salary': position.minimal_salary,
                                'other_bonus_salary': position.other_bonus_salary,
                                'razryad_coefficient': position.razryad_coefficient,
                                'razryad_value': position.razryad_value,
                                'razryad_subtract': position.razryad_subtract,
                                'right_coefficient': position.right_coefficient
                            })
                        department_list.append({
                            'id': department.id,
                            'name': department.name,
                            'positions': position_list,
                            'total_count': department.total_count,
                            'total_minimal_salary': department.total_minimal_salary,
                            'total_bonus_salary': department.total_bonus_salary,
                            'total_base_salary': department.total_base_salary,

                        })
                    documents.append({
                        'id': child.id,
                        'name': child.child_name,
                        'address': child.address,
                        'chapter_code': child.chapter_code,
                        'department_code': child.department_code,
                        'small_department_code': child.small_department_code,
                        'is_main': child.is_main,
                        'departments': department_list
                    })
                total_count = await get_count(ClientShtatkaTable)
                next_page = get_next_page(page=page+1, page_size=page_size, count=total_count, domain_name=domain_name)
                previous_page = get_prev_page(page=page+1, page_size=page_size, domain_name=domain_name)
                return dict(next=next_page, previous=previous_page, count=total_count, results=documents)
            else:
                return {}
        return {'error': 1}

    @staticmethod
    async def convert_execl(child_shtatka_id: int):
        query = 'SELECT * FROM organization_children WHERE id= :id'
        organization_child = await database.fetch_one(query=query, values={'id': child_shtatka_id})
        if organization_child:
            output = BytesIO()
            workbook = Workbook(output)
            worksheet = workbook.add_worksheet()
            cell = workbook.add_format({'color': 'black', 'font_size': 12, 'align': 'center', 'bold': 1, 'border': 1})
            cell_value = workbook.add_format({'color': 'black', 'font_size': 9, 'align': 'center', 'bold': 1})
            cell_menu = workbook.add_format({'color': 'black', 'font_size': 12, 'align': 'center', 'bold': 1, 'border': 1})
            worksheet.set_column('A:D', 12)
            worksheet.set_row(3, 30)
            worksheet.set_row(6, 30)
            worksheet.set_row(7, 30)
            worksheet.merge_range('A2:H2', 'ШТАТЛАР ЖАДВАЛИ', cell)
            worksheet.merge_range('A3:H3', '01.01.2022-yil', cell)
            worksheet.set_column('A:A', 40)
            worksheet.write('A4', 'Tashkilotning to\'liq nomi: ', cell_value)
            worksheet.set_column('B:I', 18)
            worksheet.merge_range('B4:H4', organization_child.child_name, cell_value)
            worksheet.write('A5', 'Toʼliq manzili:', cell_value)
            worksheet.merge_range('B5:H5', organization_child.address,
                                  cell_value)
            worksheet.write('A6', 'Byudjet darajasi:', cell_value)
            worksheet.merge_range('B6:C6', 'Respublika byudjeti',
                                  cell_value)
            worksheet.write('A7', 'Boʼlim:', cell_value)
            worksheet.write('B7', organization_child.chapter_code,
                                  cell_value)
            worksheet.write('A8', 'Kichik boʼlim:', cell_value)
            worksheet.write('B8', organization_child.department_code,
                            cell_value)

            worksheet.write('A9', 'Bob:', cell_value)
            worksheet.write('B9', organization_child.small_department_code,
                            cell_value)

            worksheet.set_row(10, 35)
            worksheet.write('A11', 'LАVOZIM', cell_menu)
            worksheet.write('B11', 'Shtat birlik-lari \nsoni', cell_menu)
            worksheet.write('C11', 'YaTS boʼyicha \nrazryad', cell_menu)
            worksheet.write('D11', 'Tarif koeffitsent', cell_menu)
            worksheet.write('E11', 'To\'g\'irlovchi \nkoeffitsent', cell_menu)
            worksheet.write('F11', 'Lavozimi boʼyicha \noylik ish xaqi', cell_menu)
            worksheet.write('G11', 'Ragʼbatlan-tirish \nkoeffitsent', cell_menu)
            worksheet.write('H11', 'Boshqa ustamalar', cell_menu)
            worksheet.write('I11', 'Jami ish xaqi', cell_menu)
            row = 11
            department_query = 'SELECT * FROM client_departments WHERE child_id= :child_id'
            departments = await database.fetch_all(query=department_query, values={'child_id': organization_child.id})
            for department in departments:
                row_item = row + 1
                worksheet.merge_range(row, 0, row, 8, department.name, cell_menu)
                positions = await database.fetch_all(query='SELECT * FROM client_department_positions '
                                                           'WHERE client_department_id= :client_department_id',
                                                     values={
                                                         'client_department_id': department.id
                                                     })
                for position in positions:
                    minimal_salary = '{:20,.2f}'.format(position.minimal_salary)
                    bonus_salary = '{:20,.2f}'.format(position.bonus_salary)
                    base_salary = '{:20,.2f}'.format(position.base_salary)
                    worksheet.write(row_item, 0, position.name, cell_value)
                    worksheet.write(row_item, 1, position.position_count, cell_value)
                    worksheet.write(row_item, 2, position.razryad_value, cell_value)
                    worksheet.write(row_item, 3, position.razryad_coefficient, cell_value)
                    worksheet.write(row_item, 4, position.right_coefficient, cell_value)
                    worksheet.write(row_item, 5, minimal_salary, cell_value)
                    worksheet.write(row_item, 6, bonus_salary, cell_value)
                    worksheet.write(row_item, 8, base_salary, cell_value)
                    row_item += 1
                total_minimal_salary = '{:20,.2f}'.format(department.total_minimal_salary)
                total_bonus_salary = '{:20,.2f}'.format(department.total_bonus_salary)
                total_base_salary = '{:20,.2f}'.format(department.total_base_salary)
                worksheet.write(row_item, 1, department.total_count, cell_value)
                worksheet.write(row_item, 2, 'x', cell_value)
                worksheet.write(row_item, 3, 'x', cell_value)
                worksheet.write(row_item, 5, total_minimal_salary, cell_value)
                worksheet.write(row_item, 6, total_bonus_salary, cell_value)
                worksheet.write(row_item, 8, total_base_salary, cell_value)
                row = row_item + 1
            workbook.close()
            output.seek(0)
            return output








