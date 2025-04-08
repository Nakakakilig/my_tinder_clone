from domain.models.profile import Profile
from presentation.schemas.profile import ProfileReadSchema


def profile_to_read_schema(profile: Profile) -> ProfileReadSchema:
    return ProfileReadSchema.model_validate(profile.__dict__)


def profiles_to_read_schema_list(profiles: list[Profile]) -> list[ProfileReadSchema]:
    return [profile_to_read_schema(p) for p in profiles]
