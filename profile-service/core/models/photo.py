from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .profile import Profile

from .base import Base
from .profile import Profile


class Photo(Base):
    __tablename__ = "photos"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"), index=True)
    url: Mapped[str] = mapped_column(String(100), nullable=False)

    profile: Mapped["Profile"] = relationship(back_populates="photos")
