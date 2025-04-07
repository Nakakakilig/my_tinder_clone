from datetime import datetime

from pydantic import BaseModel, Field

from domain.enums import Gender


class ProfileBaseSchema(BaseModel):
    outer_id: int = Field(..., alias="user_id", gt=0)
    first_name: str = Field(..., min_length=1, max_length=20)
    last_name: str = Field(..., min_length=1, max_length=20)
    gender: Gender
    age: int = Field(..., ge=18, le=60)
    geo_latitude: float = Field(..., gt=-90, le=90)
    geo_longitude: float = Field(..., gt=-180, le=180)

    class Config:
        populate_by_name = True


class ProfileCreateSchema(ProfileBaseSchema):
    pass


class ProfileReadSchema(ProfileBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class ProfileWithDistance(ProfileReadSchema):
    distance_km: float
