from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Photo(Base):

    __tablename__ = "photos"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"), index=True)
    url: Mapped[str] = mapped_column(String(100), nullable=False)
