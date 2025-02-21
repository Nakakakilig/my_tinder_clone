from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    created_at: datetime | None
    updated_at: datetime | None


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
