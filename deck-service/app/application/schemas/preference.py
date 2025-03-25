from datetime import datetime

from domain.enums import Gender
from pydantic import BaseModel


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
