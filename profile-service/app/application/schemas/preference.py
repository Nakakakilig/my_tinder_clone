from datetime import datetime

from domain.enums import Gender
from pydantic import BaseModel


class PreferenceBaseSchema(BaseModel):
    profile_id: int
    gender: Gender
    age: int
    radius: int


class PreferenceCreateSchema(PreferenceBaseSchema):
    pass


class PreferenceReadSchema(PreferenceBaseSchema):
    id: int
    updated_at: datetime
