from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.base import Base
from app.core.schemas.enums import Gender

if TYPE_CHECKING:
    from app.core.models.profile import Profile


class Preference(Base):
    __tablename__ = "preferences"

    profile_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("profiles.id"), index=True, unique=True
    )
    gender: Mapped[Gender] = mapped_column(Enum(Gender), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    radius: Mapped[int] = mapped_column(Integer, nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    profile: Mapped["Profile"] = relationship(back_populates="preference")
