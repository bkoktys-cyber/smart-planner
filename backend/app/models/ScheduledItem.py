from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.ScheduleRun import ScheduleRun


class ScheduledItem(Base):
    __tablename__ = "scheduled_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    schedule_run_id: Mapped[int] = mapped_column(
        ForeignKey("schedule_runs.id", ondelete="CASCADE"), index=True
    )
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    slack_hours: Mapped[int] = mapped_column(Integer)
    is_critical: Mapped[bool] = mapped_column(Boolean)

    schedule_run: Mapped["ScheduleRun"] = relationship(back_populates="items")