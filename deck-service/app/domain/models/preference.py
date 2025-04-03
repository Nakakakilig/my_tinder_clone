from datetime import datetime

from pydantic import BaseModel

from domain.enums import Gender


class Preference(BaseModel):
    profile_id: int
    gender: Gender
    age: int
    radius: int
    updated_at: datetime
