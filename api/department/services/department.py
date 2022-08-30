from api.department.schemas.department import CreateShtatDepartmentSchema
from apps.user.models import ShtatDepartmentTable, ShtatDepartmentUser, UserTable, OrganizationTable, \
    ShtatDepartmentOrganizationTable
from core.settings import database


class DepartmentService:
    @staticmethod
    async def create_department(data: CreateShtatDepartmentSchema):
        async with database.transaction():
            users = data.users
            organizations = data.organizations
            shtat_department = ShtatDepartmentTable.insert().values(
               name=data.name,
               code=data.code
            )
            shtat_department_id = await database.execute(shtat_department)
            for user_item in users:
                user = UserTable.insert().values(
                    full_name=user_item.full_name,
                    pinfl=user_item.pinfl,
                    role_id=user_item.role_id
                )
                user_id = await database.execute(user)
                shtat_department_user = ShtatDepartmentUser.insert().values(
                    user_id=user_id,
                    shtat_department_id=shtat_department_id
                )
                await database.execute(shtat_department_user)
            for organization_item in organizations:
                organization = OrganizationTable.insert().values(
                    organization_tin=organization_item.organization_tin,
                    name=organization_item.name
                )
                organization_id = await database.execute(organization)
                shtat_department_organization = ShtatDepartmentOrganizationTable.insert().values(
                    shtat_department_id=shtat_department_id,
                    organization_id=organization_id
                )
                await database.execute(shtat_department_organization)


