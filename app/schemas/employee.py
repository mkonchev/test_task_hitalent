from pydantic import BaseModel, ConfigDict
from datetime import datetime, date


class EmployeeBase(BaseModel):
    full_name: str
    position: str
    hired_at: date | None


class EmployeeCreate(BaseModel):
    full_name: str
    position: str
    hired_at: date | None


class EmployeeResponse(BaseModel):
    id: int
    full_name: str
    position: str
    hired_at: date | None
    department_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
