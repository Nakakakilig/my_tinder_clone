from datetime import datetime

from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    username: str


class UserCreateSchema(UserBaseSchema):
    pass


class UserReadSchema(UserBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
