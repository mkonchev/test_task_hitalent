import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import employee as schemas
from app.repositories.employee import EmployeeRepository
from app.repositories.department import DepartmentRepository
from app.exceptions import exceptions


class EmployeeService:
    def __init__(self, db: AsyncSession):
        self.repository = EmployeeRepository(db)
        self.department_repo = DepartmentRepository(db)

    async def create_employee(
        self,
        employee: schemas.EmployeeCreate,
        department_id: int
    ):
        if employee.full_name == "":
            raise ValueError("Zero employee fullname length")
        if employee.position == "":
            raise ValueError("Zero employee position length")
        department = await (
            self.department_repo.get_department_by_id(department_id)
        )
        if not department:
            raise exceptions.DepartmentNotFoundError(department_id)

        try:
            db_employee = await (
                self.repository.create_employee(employee, department_id)
            )
            logging.info(
                f"Employee {employee.full_name} was created in department {department_id}" # noqa
            )
            return db_employee
        except Exception as e:
            logging.error(f"Failed to create employee: {e}")
