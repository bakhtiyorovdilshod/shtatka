from pydantic import BaseModel
from typing import List


class GivePermissionSchema(BaseModel):
    permission_id: int
    user_id: int



