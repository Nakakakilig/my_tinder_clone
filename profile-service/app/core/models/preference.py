from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .user import User

import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)
from core.db.base import Base

from common.enums import Gender


class Preference(Base):
    __tablename__ = "preferences"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), index=True, unique=True
    )
    gender: Mapped[Gender] = mapped_column(Enum(Gender), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    radius: Mapped[int] = mapped_column(Integer, nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="preference")
