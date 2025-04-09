from datetime import datetime

from pydantic import BaseModel

from domain.enums import Gender


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
