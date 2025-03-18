from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db.base import Base


class Swipe(Base):
    __tablename__ = "swipes"

    user_id_1: Mapped[int] = mapped_column(nullable=False, index=True)
    user_id_2: Mapped[int] = mapped_column(nullable=False, index=True)
    decision_1: Mapped[bool] = mapped_column(nullable=True)
    decision_2: Mapped[bool] = mapped_column(nullable=True)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
