from decimal import Decimal

from fastapi import HTTPException

from api.client.schemas.document import AcceptDocumentSchema
from apps.user.models import OrganizationChildTable, ClientDepartmentTable, ClientDepartmentPositionTable
from core.settings import database


class DocumentService:
    @staticmethod
    async def accept_client_documents(data: AcceptDocumentSchema):
        async with database.transaction():
            query = 'SELECT id FROM shtat_organizations WHERE organization_tin= :organization_tin'
            organization = await database.fetch_one(query=query, values={'organization_tin': data.organization_tin})
            if not organization:
                raise HTTPException(status_code=400, detail='Access has been denied')
            for document in data.documents:
                child_organization = OrganizationChildTable.insert().values(
                    child_name=document.name,
                    address=document.address,
                    chapter_code=document.chapter_code,
                    department_code=document.department_code,
                    small_department_code=document.small_department_code,
                    parent_id=organization.id,
                    is_main=document.is_main
                )
                child_id = await database.execute(child_organization)
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
                        department_position = ClientDepartmentPositionTable.insert().values(
                            name=position.name,
                            count=position.count,
                            base_salary=position.base_salary,
                            bonus_salary=position.bonus_salary,
                            minimal_salary=position.minimal_salary,
                            other_bonus_salary=position.other_bonus_salary,
                            razryad_coefficient=position.razryad_coefficient,
                            razryad_value=position.razryad_value,
                            razryad_subtract=position.razryad_subtract,
                            client_department_id=client_department_id
                        )
                        department_position_id = await database.execute(department_position)
        return {'status': 'success'}
