from datetime import datetime
from typing import List
from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base
from app.models.employee import Employee


class Department(Base):
    """Подразделение"""
    __tablename__ = "department"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    parent_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("department.id", ondelete="SET NULL"),
        nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    children: Mapped[List["Department"]] = relationship(
        "Department",
        back_populates="parent"
    )

    parent: Mapped[List["Department"]] = relationship(
        "Department",
        back_populates="children",
        remote_side=[id]
    )

    employees: Mapped[List["Employee"]] = relationship(
        "Employee",
        back_populates="department",
    )
