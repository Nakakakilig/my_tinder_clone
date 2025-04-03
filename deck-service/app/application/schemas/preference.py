from datetime import datetime

from pydantic import BaseModel

from domain.enums import Gender


class PreferenceBase(BaseModel):
    profile_id: int
    gender: Gender
    age: int
    radius: int


class PreferenceCreate(PreferenceBase):
    pass


class PreferenceRead(PreferenceBase):
    id: int
    updated_at: datetime
