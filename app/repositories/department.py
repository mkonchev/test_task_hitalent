from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas import department as schemas
from app.models.department import Department


class DepartmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_department(
        self,
        department: schemas.DepartmnetCreate
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
