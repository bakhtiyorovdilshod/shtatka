from pydantic import BaseModel
from typing import List


class UserListCreateSchema(BaseModel):
    pinfl: str
    full_name: str
    role_id: int


class OrganizationListCreateSchema(BaseModel):
    organization_tin: str
    name: str


class CreateShtatDepartmentSchema(BaseModel):
    name: str
    code: str
    users: List[UserListCreateSchema]
    organizations: List[OrganizationListCreateSchema]