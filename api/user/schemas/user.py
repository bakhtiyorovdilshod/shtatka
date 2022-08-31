from fastapi import HTTPException, Depends
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


class UserCreateSchema(BaseModel):
    full_name: str
    pinfl: str
    username: str
    password: str
    role_id : int


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserDetailSchema(BaseModel):
    # id: int
    # full_name: str
    # username: str
    # role_id: int
    is_active: bool
