from domain.models.user import User
from presentation.schemas.user import UserReadSchema


def user_to_read_schema(user: User) -> UserReadSchema:
    return UserReadSchema.model_validate(user.__dict__)


def users_to_read_schema_list(users: list[User]) -> list[UserReadSchema]:
    return [user_to_read_schema(u) for u in users]
