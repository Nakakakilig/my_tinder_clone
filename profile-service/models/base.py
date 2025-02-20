from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):

    __tablename__ = "base"

    id: Mapped[int] = mapped_column(primary_key=True)
