from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.base import Base
from app.core.schemas.enums import Gender

if TYPE_CHECKING:
    from app.core.models.preference import Preference


class Profile(Base):
    __tablename__ = "profiles"

    outer_id: Mapped[int] = mapped_column(Integer, nullable=False)
    first_name: Mapped[str] = mapped_column(String(20), nullable=False)
    last_name: Mapped[str] = mapped_column(String(20), nullable=False)
    gender: Mapped[Gender] = mapped_column(Enum(Gender), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    geo_latitude: Mapped[float] = mapped_column(Float, nullable=False)
    geo_longitude: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    preference: Mapped["Preference"] = relationship(
        back_populates="profile", uselist=False
    )
