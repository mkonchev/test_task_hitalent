import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import department as schemas
from app.repositories.department import DepartmentRepository


class DepartmentService:
    def __init__(self, db: AsyncSession):
        self.repository = DepartmentRepository(db)

    async def create_department(self, department: schemas.DepartmnetCreate):

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
