from domain.models.preference import Preference
from infrastructure.db.db_models import PreferenceORM


def orm_to_domain(preference_orm: PreferenceORM) -> Preference:
    return Preference(
        **{
            key: value
            for key, value in preference_orm.__dict__.items()
            if key in Preference.__annotations__
        }
    )


def domain_to_orm(preference: Preference) -> PreferenceORM:
    return PreferenceORM(**preference.__dict__)
