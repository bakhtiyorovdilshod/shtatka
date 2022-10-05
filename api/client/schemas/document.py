from decimal import Decimal
from pydantic import BaseModel
from typing import List


class ListPositionSchema(BaseModel):
    name: str
    base_salary: float
    bonus_salary: float
    position_count: int
    minimal_salary: float
    other_bonus_salary: float
    razryad_coefficient: float
    razryad_subtract: int
    razryad_value: int
    right_coefficient: float


class ListDepartmentSchema(BaseModel):
    name: str
    total_base_salary: int
    total_bonus_salary: int
    total_minimal_salary: int
    total_count: int
    positions: List[ListPositionSchema]


class ListDocumentSchema(BaseModel):
    address: str
    chapter_code: str
    department_code: str
    small_department_code: str
    region: str
    district: str
    name: str
    is_main: bool
    departments: List[ListDepartmentSchema]


class DistrictDocumentSchema(BaseModel):
    address: str
    chapter_code: str
    department_code: str
    small_department_code: str
    district: str
    departments: List[ListDepartmentSchema]


class RegionDocumentSchema(BaseModel):
    address: str
    chapter_code: str
    department_code: str
    small_department_code: str
    region: str
    name: str
    departments: List[ListDepartmentSchema]
    districts: List[DistrictDocumentSchema]


class AcceptDocumentSchema(BaseModel):
    organization_tin: str
    type: str
    address: str
    chapter_code: str
    department_code: str
    small_department_code: str
    region: str
    name: str
    departments: List[ListDepartmentSchema]
    regions: List[RegionDocumentSchema]
