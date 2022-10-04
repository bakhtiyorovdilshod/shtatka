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
        delete_position_query = 'DELETE FROM client_department_positions pos ' \
                                'INNER JOIN client_departments dep ' \
                                'ON pos.client_department_id=dep.id ' \
                                'INNER JOIN organization_children child ' \
                                'ON dep.child_id=child.id WHERE child.client_shtatka_id= :client_shtatka_id'
        await database.execute(query=delete_position_query, values={'client_shtatka_id': client_shtatka.id})
        delete_department_query = 'DELETE dep FROM client_departments dep' \
                                  'INNER JOIN organization_children child' \
                                  'ON dep.child_id=child.id WHERE child.client_shtatka_id= :client_shtatka_id'
        await database.execute(query=delete_department_query, values={'client_shtatka_id': client_shtatka.id})
        delete_organization_children = 'DELETE FROM organization_children WHERE client_shtatka_id= :client_shtatka_id '
        await database.execute(query=delete_organization_children, values={'client_shtatka_id': client_shtatka.id})


        # check_query = 'SELECT id FROM organization_children WHERE client_shtatka_id= :client_shtatka_id'
        # children = await database.fetch_all(query=check_query,
        #                                     values={'client_shtatka_id': client_shtatka.id})
        # for child in children:
        #     old_department_query = 'SELECT id FROM client_departments WHERE child_id= :child_id'
        #     departments = await database.fetch_all(query=old_department_query, values={'child_id': child.id})
        #     for department in departments:
        #         position_query = 'DELETE FROM client_department_positions WHERE client_department_id= :client_department_id'
        #         await database.execute(query=position_query, values={'client_department_id': department.id})
        #     delete_department_query = 'DELETE FROM client_departments WHERE child_id= :child_id'
        #     await database.execute(query=delete_department_query, values={'child_id': child.id})
        #     await database.execute(query='DELETE FROM organization_children WHERE id= :id', values={'id': child.id})
        #     await database.execute(query='DELETE FROM client_shtatka_regions WHERE organization_child_id= :id', values={'id': child.id})

    async def create_client_position_department(self, documents, client_shtatka_id):
        position_values = []
        for document in documents:
            child = OrganizationChildTable.insert().values(
                child_name=document.name,
                address=document.address,
                chapter_code=document.chapter_code,
                department_code=document.department_code,
                small_department_code=document.small_department_code,
                is_main=document.is_main,
                client_shtatka_id=client_shtatka_id
            )
            child_id = await database.execute(child)
            # region = ClientShtatkaRegionTable.insert().values(
            #     name=document.region,
            #     organization_child_id=child_id
            # )
            # region_id = await database.execute(region)
            # district = ClientShtatkaDistrictTable.insert().values(
            #     name=document.district,
            #     client_shtatka_region_id=region_id
            # )
            # district_id = await database.execute(district)
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
                    # department_position = ClientDepartmentPositionTable.insert().values(
                    #     name=position.name,
                    #     position_count=position.position_count,
                    #     base_salary=position.base_salary,
                    #     bonus_salary=position.bonus_salary,
                    #     minimal_salary=position.minimal_salary,
                    #     other_bonus_salary=position.other_bonus_salary,
                    #     razryad_coefficient=position.razryad_coefficient,
                    #     razryad_value=position.razryad_value,
                    #     razryad_subtract=position.razryad_subtract,
                    #     client_department_id=client_department_id,
                    #     right_coefficient=position.right_coefficient
                    # )
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
                    # department_position_id = await database.execute(department_position)

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
                await self.create_client_position_department(documents=data.documents, client_shtatka_id=client_shtatka.id)
            else:
                organization_shtatka = ClientShtatkaTable.insert().values(
                    parent_id=organization.id,
                    status='pending',
                    type=data.type
                )
                client_shtatka_id = await database.execute(organization_shtatka)
                await self.create_client_position_department(documents=data.documents, client_shtatka_id=client_shtatka_id)
        return {'status': 'success'}


