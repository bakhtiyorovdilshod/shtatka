from pydantic import BaseModel
from typing import List


class PermissionListSchema(BaseModel):
    permission_id: int


class GivePermissionSchema(BaseModel):
    permissions: List[PermissionListSchema]
    user_id: int


class CreatePermissionSchema(BaseModel):
    name: str



