from sqlalchemy import DateTime, Float, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Profile(Base):

    __tablename__ = "profiles"

    username: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(20), nullable=False)
    last_name: Mapped[str] = mapped_column(String(20), nullable=False)
    geo_latitude: Mapped[float] = mapped_column(Float, nullable=False)
    geo_longitude: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
