import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas import department as schema_department
from app.schemas import employee as schema_employee
from app.services.department import DepartmentService
from app.services.employee import EmployeeService
from app.exceptions import exceptions


router = APIRouter(prefix="/departments", tags=['Departments actions'])


@router.post(
    '/',
    response_model=schema_department.DepartmentResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_department(
    department: schema_department.DepartmentCreate,
    db: AsyncSession = Depends(get_db)
):
    service = DepartmentService(db)
    try:
        return await service.create_department(department)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Exeption: {e}")


@router.post(
        '/{id}/employees',
        response_model=schema_employee.EmployeeResponse,
        status_code=status.HTTP_201_CREATED)
async def create_employee(
    id: int,
    employee: schema_employee.EmployeeCreate,
    db: AsyncSession = Depends(get_db)
):
    service = EmployeeService(db)
    try:
        employee = await (
            service.create_employee(employee, department_id=id)
        )
        return employee
    except exceptions.DepartmentNotFoundError as e:
        logging.warning(f"No department with this department_id: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Exeption: {e}")


@router.get(
    '/{department_id}',
    response_model=schema_department.DepartmentDetailResponse
)
async def get_department(
    department_id: int,
    include_employees: bool = Query(
        True,
    ),
    depth: int = Query(1, ge=1, le=5),
    db: AsyncSession = Depends(get_db)
):
    service = DepartmentService(db)
    try:
        department = await service.get_department_detail(
            department_id,
            include_employees=include_employees,
            depth=depth
        )
        return department
    except exceptions.DepartmentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.patch(
    "/{department_id}",
    response_model=schema_department.DepartmentResponse,
    status_code=status.HTTP_200_OK
)
async def update_department(
    department_id: int,
    update_data: schema_department.DepartmentUpdate,
    db: AsyncSession = Depends(get_db)
):
    service = DepartmentService(db)
    try:
        updated_department = await service.update_department(
            department_id,
            update_data
        )
        return updated_department
    except exceptions.DepartmentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except exceptions.DepartmentCycleError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
