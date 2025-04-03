from datetime import datetime

from pydantic import BaseModel, Field

from domain.enums import Gender


class ProfileBase(BaseModel):
    outer_id: int = Field(..., alias="user_id")
    first_name: str
    last_name: str
    gender: Gender
    age: int
    geo_latitude: float
    geo_longitude: float

    class Config:
        populate_by_name = True


class ProfileCreate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime


class ProfileWithDistance(BaseModel):
    profile: ProfileRead
    distance_km: float
