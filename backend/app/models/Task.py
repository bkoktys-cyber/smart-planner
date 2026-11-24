from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.Project import Project


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint("duration_hours > 0", name="ck_tasks_duration_positive"),
        CheckConstraint("priority BETWEEN 1 AND 5", name="ck_tasks_priority_range"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(200))
    duration_hours: Mapped[int] = mapped_column(Integer)
    priority: Mapped[int] = mapped_column(Integer, server_default="3")
    deadline: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), server_default="todo")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    project: Mapped["Project"] = relationship(back_populates="tasks")