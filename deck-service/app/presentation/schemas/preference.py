from datetime import datetime

from pydantic import BaseModel, Field

from domain.enums import Gender


class PreferenceBaseSchema(BaseModel):
    profile_id: int = Field(..., gt=0)
    gender: Gender
    age: int = Field(..., ge=18, le=60)
    radius: int = Field(..., gt=0, le=400)


class PreferenceCreateSchema(PreferenceBaseSchema):
    pass


class PreferenceReadSchema(PreferenceBaseSchema):
    id: int
    updated_at: datetime
