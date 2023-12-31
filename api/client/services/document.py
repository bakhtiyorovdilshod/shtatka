from decimal import Decimal

from fastapi import HTTPException

from api.client.schemas.document import AcceptDocumentSchema
from apps.user.models import OrganizationChildTable, ClientDepartmentTable, ClientDepartmentPositionTable, \
    ClientShtatkaRegionTable, ClientShtatkaDistrictTable
from apps.user.models.organization import ClientShtatkaTable
from core.settings import database
from xlsxwriter import Workbook


class DocumentService:

    async def delete_old_position_and_department(self, client_shtatka):
        delete_position_query = 'DELETE FROM client_department_positions WHERE client_department_id IN ' \
            '(SELECT client_departments.id FROM client_departments INNER JOIN organization_children ON ' \
            'client_departments.child_id=organization_children.id ' \
            'WHERE organization_children.client_shtatka_id= :client_shtatka_id) '
        await database.execute(query=delete_position_query, values={'client_shtatka_id': client_shtatka.id})
        delete_department_query = 'DELETE FROM client_departments WHERE child_id IN ' \
            '(SELECT id FROM organization_children WHERE client_shtatka_id= :client_shtatka_id)'
        await database.execute(query=delete_department_query, values={'client_shtatka_id': client_shtatka.id})
        delete_organization_children = 'DELETE FROM organization_children WHERE client_shtatka_id= :client_shtatka_id '
        delete_district_query = 'DELETE FROM client_shtatka_districts WHERE client_shtatka_region_id IN ' \
                                '(SELECT client_shtatka_regions.id FROM client_shtatka_regions INNER JOIN ' \
                                'organization_children ON ' \
                                'client_shtatka_regions.organization_child_id=organization_children.id ' \
                                'WHERE organization_children.client_shtatka_id= :client_shtatka_id)'
        await database.execute(query=delete_district_query, values={'client_shtatka_id': client_shtatka.id})
        delete_region_query = 'DELETE FROM client_shtatka_regions WHERE organization_child_id IN ' \
                              '(SELECT id FROM organization_children WHERE client_shtatka_id= :client_shtatka_id)'
        await database.execute(query=delete_region_query, values={'client_shtatka_id': client_shtatka.id})
        await database.execute(query=delete_organization_children, values={'client_shtatka_id': client_shtatka.id})

    async def create_main_client_shtatka(self, data, client_shtatka_id):
        position_values = []
        child = OrganizationChildTable.insert().values(
            child_name=data.name,
            address=data.address,
            chapter_code=data.chapter_code,
            department_code=data.department_code,
            small_department_code=data.small_department_code,
            is_republic=True,
            is_main=False,
            client_shtatka_id=client_shtatka_id
        )
        child_id = await database.execute(child)
        for department in data.departments:
            client_department = ClientDepartmentTable.insert().values(
                child_id=child_id,
                name=department.name,
                total_count=department.total_count,
                total_minimal_salary=Decimal(department.total_minimal_salary),
                total_bonus_salary=department.total_bonus_salary,
                total_base_salary=department.total_base_salary
            )
            client_department_id = await database.execute(client_department)
            for position in department.positions:
                position_values.append({
                    'name': position.name,
                    'position_count': position.position_count,
                    'base_salary': position.base_salary,
                    'bonus_salary': position.bonus_salary,
                    'minimal_salary': position.minimal_salary,
                    'other_bonus_salary': position.other_bonus_salary,
                    'razryad_coefficient': position.razryad_coefficient,
                    'razryad_value': position.razryad_value,
                    'razryad_subtract': position.razryad_subtract,
                    'client_department_id': client_department_id,
                    'right_coefficient': position.right_coefficient
                })
        query = 'INSERT INTO client_department_positions(' \
                'name, position_count, base_salary, bonus_salary, ' \
                'minimal_salary,other_bonus_salary, razryad_coefficient, razryad_value,' \
                'razryad_subtract, client_department_id, right_coefficient) VALUES (' \
                ':name, :position_count, :base_salary, :bonus_salary, :minimal_salary,' \
                ':other_bonus_salary, :razryad_coefficient, :razryad_value, :razryad_subtract,' \
                ':client_department_id, :right_coefficient)'
        await database.execute_many(query=query, values=position_values)

    async def create_client_shtatka_districts(self, districts, client_shtatka_id, region_id):
        position_values = []
        districts_list = []
        for district in districts:
            districts_list.append({
                'name': district.district,
                'client_shtatka_region_id': region_id
            })
            child = OrganizationChildTable.insert().values(
                child_name=district.name,
                address=district.address,
                chapter_code=district.chapter_code,
                department_code=district.department_code,
                small_department_code=district.small_department_code,
                is_main=False,
                client_shtatka_id=client_shtatka_id
            )
            child_id = await database.execute(child)
            for department in district.departments:
                client_department = ClientDepartmentTable.insert().values(
                    child_id=child_id,
                    name=department.name,
                    total_count=department.total_count,
                    total_minimal_salary=Decimal(department.total_minimal_salary),
                    total_bonus_salary=department.total_bonus_salary,
                    total_base_salary=department.total_base_salary
                )
                client_department_id = await database.execute(client_department)
                for position in department.positions:
                    position_values.append({
                        'name': position.name,
                        'position_count': position.position_count,
                        'base_salary': position.base_salary,
                        'bonus_salary': position.bonus_salary,
                        'minimal_salary': position.minimal_salary,
                        'other_bonus_salary': position.other_bonus_salary,
                        'razryad_coefficient': position.razryad_coefficient,
                        'razryad_value': position.razryad_value,
                        'razryad_subtract': position.razryad_subtract,
                        'client_department_id': client_department_id,
                        'right_coefficient': position.right_coefficient
                    })
        query = 'INSERT INTO client_department_positions(' \
                'name, position_count, base_salary, bonus_salary, ' \
                'minimal_salary,other_bonus_salary, razryad_coefficient, razryad_value,' \
                'razryad_subtract, client_department_id, right_coefficient) VALUES (' \
                ':name, :position_count, :base_salary, :bonus_salary, :minimal_salary,' \
                ':other_bonus_salary, :razryad_coefficient, :razryad_value, :razryad_subtract,' \
                ':client_department_id, :right_coefficient)'
        district_query = 'INSERT INTO client_shtatka_districts(' \
                         'name, client_shtatka_region_id) VALUES (' \
                         ':name, :client_shtatka_region_id)'
        await database.execute_many(query=district_query, values=districts_list)
        await database.execute_many(query=query, values=position_values)

    async def create_client_shtatka_regions(self, data, client_shtatka_id):
        await self.create_main_client_shtatka(data=data, client_shtatka_id=client_shtatka_id)
        position_values = []
        for document in data.regions:
            child = OrganizationChildTable.insert().values(
                child_name=document.name,
                address=document.address,
                chapter_code=document.chapter_code,
                department_code=document.department_code,
                small_department_code=document.small_department_code,
                is_main=True,
                client_shtatka_id=client_shtatka_id
            )
            child_id = await database.execute(child)
            region = ClientShtatkaRegionTable.insert().values(
                name=document.region,
                organization_child_id=child_id
            )
            region_id = await database.execute(region)
            for department in document.departments:
                client_department = ClientDepartmentTable.insert().values(
                    child_id=child_id,
                    name=department.name,
                    total_count=department.total_count,
                    total_minimal_salary=Decimal(department.total_minimal_salary),
                    total_bonus_salary=department.total_bonus_salary,
                    total_base_salary=department.total_base_salary
                )
                client_department_id = await database.execute(client_department)
                for position in department.positions:
                    position_values.append({
                        'name': position.name,
                        'position_count': position.position_count,
                        'base_salary': position.base_salary,
                        'bonus_salary': position.bonus_salary,
                        'minimal_salary': position.minimal_salary,
                        'other_bonus_salary': position.other_bonus_salary,
                        'razryad_coefficient': position.razryad_coefficient,
                        'razryad_value': position.razryad_value,
                        'razryad_subtract': position.razryad_subtract,
                        'client_department_id': client_department_id,
                        'right_coefficient': position.right_coefficient
                    })
            await self.create_client_shtatka_districts(districts=document.districts, client_shtatka_id=client_shtatka_id, region_id=region_id)
        query = 'INSERT INTO client_department_positions(' \
                'name, position_count, base_salary, bonus_salary, ' \
                'minimal_salary,other_bonus_salary, razryad_coefficient, razryad_value,' \
                'razryad_subtract, client_department_id, right_coefficient) VALUES (' \
                ':name, :position_count, :base_salary, :bonus_salary, :minimal_salary,' \
                ':other_bonus_salary, :razryad_coefficient, :razryad_value, :razryad_subtract,' \
                ':client_department_id, :right_coefficient)'
        await database.execute_many(query=query, values=position_values)

    async def accept_client_documents(self, data: AcceptDocumentSchema):
        async with database.transaction():
            if data.type not in ['with_self', 'with_budget']:
                raise HTTPException(status_code=400, detail='type has not been matched')
            query = 'SELECT id FROM shtat_organizations WHERE organization_tin= :organization_tin'
            organization = await database.fetch_one(query=query, values={'organization_tin': data.organization_tin})
            if not organization:
                raise HTTPException(status_code=400, detail='Access has been denied')
            client_shtatka = await database.fetch_one(
                query='SELECT id FROM client_shtatkas WHERE parent_id= :parent_id and type= :type', values={
                    'parent_id': organization.id,
                    'type': data.type
                })
            if client_shtatka:
                await database.execute(query='UPDATE client_shtatkas SET shtatka_status= :shtatka_status, type= :type WHERE parent_id= :parent_id', values={
                    'shtatka_status': 'pending',
                    'parent_id': organization.id,
                    'type': data.type
                })
                await self.delete_old_position_and_department(client_shtatka=client_shtatka)
                await self.create_client_shtatka_regions(data=data, client_shtatka_id=client_shtatka.id)
            else:
                organization_shtatka = ClientShtatkaTable.insert().values(
                    parent_id=organization.id,
                    status='pending',
                    type=data.type
                )
                client_shtatka_id = await database.execute(organization_shtatka)
                await self.create_client_shtatka_regions(data=data, client_shtatka_id=client_shtatka_id)
        return {'status': 'success'}


