from datetime import datetime

from domain.enums import EventType, Gender
from pydantic import BaseModel


class PreferenceBaseSchema(BaseModel):
    profile_id: int
    gender: Gender
    age: int
    radius: int


class PreferenceCreateSchema(PreferenceBaseSchema):
    pass


class PreferenceReadSchema(PreferenceBaseSchema):
    id: int
    updated_at: datetime


class PreferenceCreatedEvent(PreferenceBaseSchema):
    event_type: str = EventType.PREFERENCE_CREATED.value
    occurred_at: datetime
