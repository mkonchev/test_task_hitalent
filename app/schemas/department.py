from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.employee import EmployeeResponse


class DepartmentBase(BaseModel):
    name: str
    parent_id: int | None


class DepartmentCreate(BaseModel):
    name: str
    parent_id: int | None = None


class DepartmentResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class DepartmentDetailResponce(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime | None
    employees: list[EmployeeResponse] = []
    children: list['DepartmentDetailResponce'] = []

    model_config = ConfigDict(from_attributes=True)


DepartmentDetailResponce.model_rebuild()
