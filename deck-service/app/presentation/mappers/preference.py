from application.schemas.preference import PreferenceReadSchema
from domain.models.preference import Preference


def preference_to_read_schema(preference: Preference) -> PreferenceReadSchema:
    return PreferenceReadSchema.model_validate(preference.__dict__)


def preferences_to_read_schema_list(preferences: list[Preference]) -> list[PreferenceReadSchema]:
    return [preference_to_read_schema(p) for p in preferences]
