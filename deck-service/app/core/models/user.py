from typing import TYPE_CHECKING

from core.db.base import Base
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .photo import Photo
    from .profile import Profile


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    profile: Mapped["Profile"] = relationship(back_populates="user", uselist=False)
    photos: Mapped[list["Photo"]] = relationship(back_populates="user")
