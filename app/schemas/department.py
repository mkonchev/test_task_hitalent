from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from enum import Enum
from app.schemas.employee import EmployeeResponse


class DepartmentBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    parent_id: int | None


class DepartmentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    parent_id: int | None = None


class DepartmentUpdate(BaseModel):
    name: str | None = Field(min_length=1, max_length=200)
    parent_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class DeleteMode(str, Enum):
    CASCADE = "cascade"
    REASSIGN = "reassign"


class DepartmentDeleteQuery(BaseModel):
    mode: DeleteMode
    reassign_to_department_id: int | None = None

    model_config = ConfigDict(extra="forbid")


class DepartmentResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DepartmentDetailResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    employees: list[EmployeeResponse] = []
    children: list['DepartmentDetailResponse'] = []

    model_config = ConfigDict(from_attributes=True)


DepartmentDetailResponse.model_rebuild()
