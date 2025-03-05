# from typing import TYPE_CHECKING

# from core.db.base import Base
# from sqlalchemy import ForeignKey, Integer, String
# from sqlalchemy.orm import Mapped, mapped_column, relationship

# if TYPE_CHECKING:
#     from .user import User


# class Photo(Base):
#     __tablename__ = "photos"

#     user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
#     url: Mapped[str] = mapped_column(String(100), nullable=False)

#     user: Mapped["User"] = relationship(back_populates="photos")
