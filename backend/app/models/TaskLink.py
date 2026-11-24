from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TaskLink(Base):
    __tablename__ = "task_links"
    __table_args__ = (
        UniqueConstraint("predecessor_id", "successor_id", name="uq_task_links_pair"),
        CheckConstraint("predecessor_id <> successor_id", name="ck_task_links_not_self"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    predecessor_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"), index=True
    )
    successor_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"), index=True
    )