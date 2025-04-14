from unittest.mock import AsyncMock

import pytest
from aiokafka.errors import KafkaConnectionError  # type: ignore

from app.domain.enums import Gender
from app.domain.exceptions import ProfileAlreadyExistsError, ProfileCreateError
from app.domain.models.profile import Profile
from app.presentation.schemas.profile import ProfileCreateSchema
from app.use_cases.profile import ProfileService


async def test_create_profile():
    mock_profile_repository = AsyncMock()
    mock_kafka_producer = AsyncMock()
    service = ProfileService(
        profile_repository=mock_profile_repository, kafka_producer=mock_kafka_producer
    )

    test_profile = Profile(
        user_id=123,
        first_name="John",
        last_name="Doe",
        gender=Gender.male,
        age=30,
        geo_latitude=50.0,
        geo_longitude=60.0,
    )

    saved_profile = Profile(
        **test_profile.__dict__,  # no id and timestamp in mock
    )
    mock_profile_repository.create_profile.return_value = saved_profile

    result = await service.create_profile(test_profile)
    assert result == saved_profile

    mock_profile_repository.create_profile.assert_awaited_once_with(test_profile)

    profile_data = ProfileCreateSchema.model_validate(saved_profile.__dict__).model_dump()

    mock_kafka_producer.send_event.assert_awaited_once()
    called_args = mock_kafka_producer.send_event.call_args[0]
    topic_arg = called_args[0]
    event_arg = called_args[1]

    assert topic_arg == "profile-events"
    assert event_arg["event_type"] == "profile_created"
    assert event_arg["data"] == profile_data
    assert "timestamp" in event_arg

    assert result == saved_profile
    assert result.id is None
    assert result.first_name == "John"


async def test_create_bad_profile_gender():
    mock_profile_repository = AsyncMock()
    mock_kafka_producer = AsyncMock()
    service = ProfileService(
        profile_repository=mock_profile_repository, kafka_producer=mock_kafka_producer
    )
    test_profile = Profile(
        user_id=123,
        first_name="John",
        last_name="Doe",
        gender=123,  # type: ignore
        age=30,
        geo_latitude=50.0,
        geo_longitude=60.0,
    )

    saved_profile = Profile(
        **test_profile.__dict__,  # no id and timestamp in mock
    )
    mock_profile_repository.create_profile.return_value = saved_profile

    with pytest.raises(ValueError):  # type: ignore
        await service.create_profile(test_profile)


async def test_create_bad_profile_first_name():
    mock_profile_repository = AsyncMock()
    mock_kafka_producer = AsyncMock()
    service = ProfileService(
        profile_repository=mock_profile_repository, kafka_producer=mock_kafka_producer
    )
    test_profile = Profile(
        user_id=123,
        first_name=-1,  # type: ignore
        last_name="Doe",
        gender=Gender.male,
        age=30,
        geo_latitude=50.0,
        geo_longitude=60.0,
    )

    saved_profile = Profile(
        **test_profile.__dict__,  # no id and timestamp in mock
    )
    mock_profile_repository.create_profile.return_value = saved_profile

    with pytest.raises(ValueError):  # type: ignore
        await service.create_profile(test_profile)


async def test_create_profile_already_exists():
    mock_profile_repository = AsyncMock()
    mock_kafka_producer = AsyncMock()
    service = ProfileService(
        profile_repository=mock_profile_repository, kafka_producer=mock_kafka_producer
    )

    test_profile = Profile(
        user_id=123,
        first_name="John",
        last_name="Doe",
        gender=Gender.male,
        age=30,
        geo_latitude=50.0,
        geo_longitude=60.0,
    )
    mock_profile_repository.create_profile.side_effect = ProfileAlreadyExistsError(user_id=123)

    with pytest.raises(ProfileAlreadyExistsError):
        await service.create_profile(test_profile)

    mock_profile_repository.create_profile.assert_called_once_with(test_profile)


async def test_create_profile_create_error():
    mock_profile_repository = AsyncMock()
    mock_kafka_producer = AsyncMock()
    service = ProfileService(
        profile_repository=mock_profile_repository, kafka_producer=mock_kafka_producer
    )

    test_profile = Profile(
        user_id=123,
        first_name="John",
        last_name="Doe",
        gender=Gender.male,
        age=30,
        geo_latitude=50.0,
        geo_longitude=60.0,
    )
    mock_profile_repository.create_profile.side_effect = ProfileCreateError(user_id=123)

    with pytest.raises(ProfileCreateError):
        await service.create_profile(test_profile)

    mock_profile_repository.create_profile.assert_called_once_with(test_profile)


async def test_create_profile_kafka_connection_error():
    mock_profile_repository = AsyncMock()
    mock_kafka_producer = AsyncMock()
    service = ProfileService(
        profile_repository=mock_profile_repository, kafka_producer=mock_kafka_producer
    )

    test_profile = Profile(
        user_id=123,
        first_name="John",
        last_name="Doe",
        gender=Gender.male,
        age=30,
        geo_latitude=50.0,
        geo_longitude=60.0,
    )
    mock_profile_repository.create_profile.side_effect = KafkaConnectionError()

    with pytest.raises(KafkaConnectionError):
        await service.create_profile(test_profile)

    mock_profile_repository.create_profile.assert_called_once_with(test_profile)


async def test_create_profile_empty_profile():
    with pytest.raises(TypeError):
        Profile()  # type: ignore
