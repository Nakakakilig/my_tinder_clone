from datetime import datetime

from domain.enums import EventType, Gender
from pydantic import BaseModel


class ProfileBaseSchema(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    gender: Gender
    age: int
    geo_latitude: float
    geo_longitude: float


class ProfileCreateSchema(ProfileBaseSchema):
    pass


class ProfileReadSchema(ProfileBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class ProfileCreatedEvent(ProfileBaseSchema):
    event_type: str = EventType.PROFILE_CREATED.value
    occurred_at: datetime
