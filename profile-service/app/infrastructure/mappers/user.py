from domain.models.user import User
from infrastructure.db.db_models import UserORM


# todo: do with Generic
def orm_to_domain(user_orm: UserORM) -> User:
    return User(
        **{key: value for key, value in user_orm.__dict__.items() if key in User.__annotations__}
    )


def domain_to_orm(user: User) -> UserORM:
    return UserORM(**user.__dict__)
