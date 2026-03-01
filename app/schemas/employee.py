from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date


class EmployeeBase(BaseModel):
    full_name: str = Field(min_length=1, max_length=200)
    position: str = Field(min_length=1, max_length=200)
    hired_at: date | None


class EmployeeCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=200)
    position: str = Field(min_length=1, max_length=200)
    hired_at: date | None


class EmployeeResponse(BaseModel):
    id: int
    full_name: str = Field(min_length=1, max_length=200)
    position: str = Field(min_length=1, max_length=200)
    hired_at: date | None
    department_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
