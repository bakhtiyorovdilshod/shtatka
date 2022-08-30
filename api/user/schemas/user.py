from pydantic import BaseModel, validator
from typing import List

from sqlalchemy import select

from apps.user.models import UserRoleTable
from core.settings import database


class UpdateOrganizationSchema(BaseModel):
    chapter_code: str
    department_code: str
    small_department_code: str


class CreateRoleSchema(BaseModel):
     name: str

     # @validator("name")
     # async def unique_name(cls, value):
     #     role = select[UserRoleTable].where(name=value)
     #     result = await database.fetch_all(role)
