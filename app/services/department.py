import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import department as schemas_department
from app.schemas import employee as schemas_employee
from app.repositories.department import DepartmentRepository
from app.exceptions import exceptions
from app.repositories.employee import EmployeeRepository


class DepartmentService:
    def __init__(self, db: AsyncSession):
        self.repository = DepartmentRepository(db)
        self.repository_employee = EmployeeRepository(db)

    async def create_department(
        self,
        department: schemas_department.DepartmentCreate
    ):

        if department.name == "":
            raise ValueError("Zero department name length")
        if department.parent_id is not None:
            parent = await (
                self.repository.get_department_by_id(department.parent_id)
            )
            if not parent:
                raise ValueError("Parent department with this id not found")

        existing = await (
            self.repository.get_department_by_parent(department.parent_id)
        )
        if any(dept.name == department.name for dept in existing):
            raise ValueError(
                "Department with this name already exists under this parent"
            )

        try:
            db_department = await self.repository.create_department(department)
            logging.info(f"Department {department.name} created")
            return db_department
        except Exception as e:
            logging.error(f"Can't to create Department. Error {e}")

    async def get_department_by_id(self, department_id: int):
        department = await (
            self.repository.get_department_by_id(department_id)
        )
        return department

    async def get_department_detail(
        self,
        department_id: int,
        include_employees: bool = True,
        depth: int = 1
    ):
        department_model = await self.repository.get_department_by_id(
            department_id
        )

        if not department_model:
            raise exceptions.DepartmentNotFoundError(department_id)

        department_data = schemas_department.DepartmentDetailResponse(
            id=department_model.id,
            name=department_model.name,
            created_at=department_model.created_at,
            employees=[],
            children=[]
        )

        if include_employees:
            employees_models = await (
                self.repository_employee.get_employees_by_department(
                    department_id
                )
            )
            department_data.employees = [
                schemas_employee.EmployeeResponse(
                    id=emp.id,
                    full_name=emp.full_name,
                    position=emp.position,
                    hired_at=emp.hired_at,
                    department_id=emp.department_id,
                    created_at=emp.created_at
                )
                for emp in employees_models
            ]

        if depth > 0:
            department_data.children = await self._get_child_departments(
                department_id,
                include_employees=include_employees,
                current_depth=1,
                max_depth=depth
            )

        return department_data

    async def _get_child_departments(
        self,
        parent_id: int,
        include_employees: bool,
        current_depth: int,
        max_depth: int
    ) -> list[schemas_department.DepartmentDetailResponse]:

        child_models = await self.repository.get_child_departments(parent_id)

        result = []
        for child_model in child_models:

            child_data = schemas_department.DepartmentDetailResponse(
                id=child_model.id,
                name=child_model.name,
                created_at=child_model.created_at,
                employees=[],
                children=[]
            )

            if include_employees:
                employees_models = await (
                    self.repository_employee.get_employees_by_department(
                        child_model.id
                    )
                )
                child_data.employees = [
                    schemas_employee.EmployeeResponse(
                        id=emp.id,
                        full_name=emp.full_name,
                        position=emp.position,
                        hired_at=emp.hired_at,
                        department_id=emp.department_id,
                        created_at=emp.created_at
                    )
                    for emp in employees_models
                ]

            if current_depth < max_depth:
                child_data.children = await self._get_child_departments(
                    child_model.id,
                    include_employees=include_employees,
                    current_depth=current_depth + 1,
                    max_depth=max_depth
                )

            result.append(child_data)

        return result
