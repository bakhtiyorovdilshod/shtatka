from pydantic import BaseModel
from typing import List


class UpdateOrganizationSchema(BaseModel):
    chapter_code: str
    department_code: str
    small_department_code: str
