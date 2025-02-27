from datetime import datetime

from pydantic import BaseModel

from core.db.enums import Gender


class ProfileBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    gender: Gender
    geo_latitude: float
    geo_longitude: float


class ProfileCreate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime
