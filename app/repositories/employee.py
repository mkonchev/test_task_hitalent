from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas import employee as schemas
from app.models.employee import Employee


class EmployeeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_employee(
        self,
        employee: schemas.EmployeeCreate,
        department_id: int
    ):
        db_employee = Employee(
            full_name=employee.full_name,
            position=employee.position,
            hired_at=employee.hired_at,
            department_id=department_id
        )
        self.db.add(db_employee)
        await self.db.commit()
        await self.db.refresh(db_employee)
        return db_employee

    async def get_employee_by_id(self, id: int) -> Employee:
        result = await self.db.execute(
            select(Employee).where(Employee.id == id)
        )
        return result.scalar_one_or_none()

    async def get_employees_by_name_in_department(
        self,
        department_id: int,
        full_name: str
    ) -> Employee | None:
        result = await self.db.execute(
            select(Employee).where(
                Employee.department_id == department_id,
                Employee.full_name == full_name
            )
        )
        return result.scalar_one_or_none()
