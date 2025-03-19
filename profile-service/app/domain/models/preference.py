from datetime import datetime

from domain.enums import Gender
from pydantic import BaseModel


class Preference(BaseModel):
    id: int
    profile_id: int
    gender: Gender
    age: int
    radius: int
    updated_at: datetime
