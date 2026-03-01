from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from app.schemas import department as schemas
from app.models.department import Department
from app.models.employee import Employee


class DepartmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_department(
        self,
        department: schemas.DepartmentCreate
    ) -> Department | None:
        db_department = Department(
            name=department.name,
            parent_id=department.parent_id,
        )
        self.db.add(db_department)
        await self.db.commit()
        await self.db.refresh(db_department)
        return db_department

    async def get_department_by_id(self, id: int) -> Department | None:
        result = await self.db.execute(
            select(Department).where(Department.id == id)
        )
        return result.scalar_one_or_none()

    async def get_department_by_name(self, name: str) -> Department | None:
        result = await self.db.execute(
            select(Department).where(Department.name == name)
        )
        return result.scalar_one_or_none()

    async def get_department_by_parent(
        self,
        parent_id: int | None = None
    ) -> list[Department]:
        query = select(Department)
        if parent_id is not None:
            query = query.where(Department.parent_id == parent_id)
        else:
            query = query.where(Department.parent_id.is_(None))

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_department_with_employees(
        self,
        id: int
    ) -> Department | None:
        result = await self.db.execute(
            select(Department)
            .where(Department.id == id)
            .options(selectinload(Department.employees))
        )
        return result.scalar_one_or_none()

    async def get_department_detail(
        self,
        id: int,
        include_employees: bool = True
    ) -> Department | None:
        query = select(Department).where(Department.id == id)

        if include_employees:
            query = query.options(
                selectinload(Department.employees)
                .selectin(Employee).order_by(Employee.full_name)
            )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_child_departments(self, parent_id: int) -> list[Department]:
        result = await self.db.execute(
            select(Department)
            .where(Department.parent_id == parent_id)
            .order_by(Department.name)
        )
        return result.scalars().all()
