from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, String, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.department import Department


class Employee(Base):
    """Сотрудник"""
    __tablename__ = 'employee'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    department_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("department.id", ondelete="SET NULL"),
        nullable=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    position: Mapped[str] = mapped_column(String(200), nullable=False)
    hired_at: Mapped[datetime | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    department: Mapped["Department"] = relationship(
        "Department",
        back_populates="employees"
    )
