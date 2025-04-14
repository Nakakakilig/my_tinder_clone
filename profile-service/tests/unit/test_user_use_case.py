from unittest.mock import AsyncMock

import pytest

from app.domain.exceptions import UserAlreadyExistsError, UserCreateError
from app.domain.models.user import User
from app.use_cases.user import UserService


async def test_create_profile():
    mock_user_repository = AsyncMock()
    service = UserService(user_repository=mock_user_repository)

    test_user = User(
        username="John",
    )

    saved_user = User(
        **test_user.__dict__,  # no id and timestamp in mock
    )
    mock_user_repository.create_user.return_value = saved_user

    result = await service.create_user(test_user)
    assert result == saved_user


async def test_get_user_by_id():
    mock_user_repository = AsyncMock()
    service = UserService(user_repository=mock_user_repository)

    test_user = User(
        id=123,
        username="John",
    )

    saved_user = User(
        **test_user.__dict__,  # no id and timestamp in mock
    )
    mock_user_repository.get_user_by_id.return_value = saved_user
    result = await service.get_user_by_id(test_user.id)  # type: ignore
    assert result == saved_user


async def test_get_user_by_username():
    mock_user_repository = AsyncMock()
    service = UserService(user_repository=mock_user_repository)

    test_user = User(
        username="John",
    )

    saved_user = User(
        **test_user.__dict__,  # no id and timestamp in mock
    )
    mock_user_repository.get_user_by_username.return_value = saved_user

    result = await service.get_user_by_username(test_user.username)
    assert result == saved_user


async def test_get_user_by_username_not_found():
    mock_user_repository = AsyncMock()
    service = UserService(user_repository=mock_user_repository)

    mock_user_repository.get_user_by_username.return_value = None

    result = await service.get_user_by_username("non_existent_user")
    assert result is None


async def test_create_user_already_exists():
    mock_user_repository = AsyncMock()
    service = UserService(mock_user_repository)

    test_user = User(username="John")
    mock_user_repository.create_user.side_effect = UserAlreadyExistsError(username="John")

    with pytest.raises(UserAlreadyExistsError):
        await service.create_user(test_user)

    mock_user_repository.create_user.assert_called_once_with(test_user)


async def test_create_user_create_error():
    mock_user_repository = AsyncMock()
    service = UserService(mock_user_repository)

    test_user = User(username="John")
    mock_user_repository.create_user.side_effect = UserCreateError(username="John")

    with pytest.raises(UserCreateError):
        await service.create_user(test_user)

    mock_user_repository.create_user.assert_called_once_with(test_user)


async def test_create_user_empty_user():
    with pytest.raises(TypeError):
        User()  # type: ignore
