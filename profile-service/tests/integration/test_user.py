import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.user import User
from app.infrastructure.repositories_impl.user import UserRepositoryImpl
from app.use_cases.user import UserService


# @pytest.mark.asyncio(loop_scope="session")
# async def test_create_user_integration(db_session: AsyncSession):
#     user_repo = UserRepositoryImpl(db_session=db_session)
#     service = UserService(user_repository=user_repo)

#     test_user = User(username="john_integration_test")
#     new_user = await service.create_user(test_user)

#     assert new_user.id is not None

#     user_in_db = await user_repo.get_user_by_id(new_user.id)
#     assert user_in_db is not None
#     assert user_in_db.username == "john_integration_test"


# @pytest.mark.asyncio(loop_scope="session")
# async def test_create_second_user_integration(db_session: AsyncSession):
#     user_repo = UserRepositoryImpl(db_session=db_session)
#     service = UserService(user_repository=user_repo)

#     test_user = User(username="john_integration_test_2")
#     new_user = await service.create_user(test_user)

#     assert new_user.id is not None

#     user_in_db = await user_repo.get_user_by_id(new_user.id)
#     assert user_in_db is not None
#     assert user_in_db.username == "john_integration_test_2"
