from datetime import datetime

from domain.enums import Gender
from pydantic import BaseModel


class Profile(BaseModel):
    outer_id: int
    first_name: str
    last_name: str
    gender: Gender
    age: int
    geo_latitude: float
    geo_longitude: float
    created_at: datetime
    updated_at: datetime
