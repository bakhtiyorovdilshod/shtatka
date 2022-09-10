from decimal import Decimal
from pydantic import BaseModel
from typing import List


class ListPositionSchema(BaseModel):
    name: str
    base_salary: Decimal
    bonus_salary: Decimal
    count: int
    minimal_salary: Decimal
    other_bonus_salary: Decimal
    razryad_coefficient: Decimal
    razryad_subtract: int
    razryad_value: int
    right_coefficient: Decimal


class ListDepartmentSchema(BaseModel):
    name: str
    total_base_salary: Decimal
    total_bonus_salary: Decimal
    total_minimal_salary: Decimal
    total_count: int
    positions: List[ListPositionSchema]


class ListDocumentSchema(BaseModel):
    address: str
    chapter_code: str
    department_code: str
    small_department_code: str
    is_main: bool
    departments: List[ListDepartmentSchema]


class AcceptDocumentSchema(BaseModel):
    organization_inn: str
    documents: List[ListDocumentSchema]
