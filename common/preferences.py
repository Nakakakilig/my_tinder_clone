from datetime import datetime

from pydantic import BaseModel

from .enums import Gender


class PreferenceBase(BaseModel):
    user_id: int
    gender: Gender
    age: int
    radius: int


class PreferenceCreate(PreferenceBase):
    pass


class PreferenceRead(PreferenceBase):
    id: int
    updated_at: datetime
