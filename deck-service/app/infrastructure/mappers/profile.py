from domain.models.profile import Profile
from infrastructure.db.db_models import ProfileORM


def orm_to_domain(profile_orm: ProfileORM) -> Profile:
    return Profile(
        **{
            key: value
            for key, value in profile_orm.__dict__.items()
            if key in Profile.__annotations__
        }
    )


def domain_to_orm(profile: Profile) -> ProfileORM:
    return ProfileORM(**profile.__dict__)
