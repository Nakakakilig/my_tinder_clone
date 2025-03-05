from datetime import datetime
from pydantic import BaseModel
from .enums import Gender


class ProfileBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    gender: Gender
    age: int
    geo_latitude: float
    geo_longitude: float


class ProfileCreate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime


class ProfileWithDistance(BaseModel):
    profile: ProfileRead
    distance_km: float
