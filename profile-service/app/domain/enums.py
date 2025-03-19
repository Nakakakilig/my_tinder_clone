import enum


class Gender(enum.Enum):
    male = "male"
    female = "female"


class EventType(enum.Enum):
    USER_CREATED = "user_created"
    PROFILE_CREATED = "profile_created"
    PREFERENCE_CREATED = "preference_created"
