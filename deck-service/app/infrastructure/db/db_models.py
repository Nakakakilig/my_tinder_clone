from domain.enums import Gender
from infrastructure.db.base import Base
from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ProfileORM(Base):
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

    preference: Mapped["PreferenceORM"] = relationship(
        back_populates="profile", uselist=False, lazy="selectin"
    )


class PreferenceORM(Base):
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

    profile: Mapped["ProfileORM"] = relationship(back_populates="preference")


# class PhotoORM(Base):
#     __tablename__ = "photos"

#     profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"), index=True)
#     url: Mapped[str] = mapped_column(String(100), nullable=False)

#     profile: Mapped["ProfileORM"] = relationship(back_populates="photos")
