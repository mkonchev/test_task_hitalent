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

    async def _check_for_cycles(
        self,
        department_id: int,
        new_parent_id: int | None
    ) -> bool:
        if new_parent_id is None:
            return False

        current_parent_id = new_parent_id
        visited = {department_id}

        while current_parent_id is not None:
            if current_parent_id in visited:
                return True

            visited.add(current_parent_id)

            parent_dept = await (
                self.repository.get_department_by_id(current_parent_id)
            )
            if parent_dept is None:
                break

            current_parent_id = parent_dept.parent_id

        return False

    async def update_department(
        self,
        department_id: int,
        update_data: schemas_department.DepartmentUpdate
    ):
        existing_department = await (
            self.repository.get_department_by_id(department_id)
        )
        if not existing_department:
            raise exceptions.DepartmentNotFoundError(department_id)

        update_values = {}

        if update_data.name is not None:
            if update_data.name == "":
                raise ValueError("Department name cannot be empty")
            update_values["name"] = update_data.name

        if update_data.parent_id is not None:
            if update_data.parent_id == department_id:
                raise ValueError("Department cannot be its own parent")

            if update_data.parent_id is not None:
                parent = await (
                    self.repository.get_department_by_id(update_data.parent_id)
                )
                if not parent:
                    raise ValueError(f"Parent department with id {update_data.parent_id} not found") # noqa

            if await (
                self._check_for_cycles(department_id, update_data.parent_id)
            ):
                raise exceptions.DepartmentCycleError(
                    f"Moving department {department_id} under {update_data.parent_id} would create a cycle" # noqa
                )

            update_values["parent_id"] = update_data.parent_id

        if "name" in update_values or "parent_id" in update_values:
            check_parent_id = update_values.get(
                "parent_id",
                existing_department.parent_id
            )
            check_name = update_values.get("name", existing_department.name)

            siblings = await (
                self.repository.get_department_by_parent(check_parent_id)
            )
            for sibling in siblings:
                if sibling.id != department_id and sibling.name == check_name:
                    raise ValueError(
                        f"Department with name '{check_name}' already exists under this parent"  # noqa
                    )

        try:
            updated_department = await self.repository.update_department(
                department_id,
                update_values
            )
            logging.info(
                f"Department {department_id} updated with: {update_values}"
            )
            return updated_department
        except Exception as e:
            logging.error(f"Failed to update department {department_id}: {e}")
            raise
