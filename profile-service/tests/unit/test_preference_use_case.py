from unittest.mock import AsyncMock

import pytest
from aiokafka.errors import KafkaConnectionError  # type: ignore

from app.domain.enums import Gender
from app.domain.exceptions import PreferenceAlreadyExistsError, PreferenceCreateError
from app.domain.models.preference import Preference
from app.presentation.schemas.preference import PreferenceCreateSchema
from app.use_cases.preference import PreferenceService


async def test_create_profile():
    mock_preference_repository = AsyncMock()
    mock_kafka_producer = AsyncMock()
    service = PreferenceService(
        preference_repository=mock_preference_repository, kafka_producer=mock_kafka_producer
    )

    test_preference = Preference(
        profile_id=123,
        gender=Gender.male,
        age=30,
        radius=100,
    )

    saved_preference = Preference(
        **test_preference.__dict__,  # no id and timestamp in mock
    )
    mock_preference_repository.create_preference.return_value = saved_preference

    result = await service.create_preference(test_preference)
    assert result == saved_preference

    mock_preference_repository.create_preference.assert_awaited_once_with(test_preference)

    preference_data = PreferenceCreateSchema.model_validate(saved_preference.__dict__).model_dump()

    mock_kafka_producer.send_event.assert_awaited_once()
    called_args = mock_kafka_producer.send_event.call_args[0]
    topic_arg = called_args[0]
    event_arg = called_args[1]

    assert topic_arg == "profile-events"
    assert event_arg["event_type"] == "preference_created"
    assert event_arg["data"] == preference_data
    assert "timestamp" in event_arg

    assert result == saved_preference
    assert result.id is None


async def test_create_bad_preference_gender():
    mock_preference_repository = AsyncMock()
    mock_kafka_producer = AsyncMock()
    service = PreferenceService(
        preference_repository=mock_preference_repository, kafka_producer=mock_kafka_producer
    )
    test_preference = Preference(
        profile_id=123,
        gender=123,  # type: ignore
        age=30,
        radius=100,
    )

    saved_preference = Preference(
        **test_preference.__dict__,  # no id and timestamp in mock
    )
    mock_preference_repository.create_preference.return_value = saved_preference

    with pytest.raises(ValueError):  # type: ignore
        await service.create_preference(test_preference)


async def test_create_preference_already_exists():
    mock_preference_repository = AsyncMock()
    mock_kafka_producer = AsyncMock()
    service = PreferenceService(
        preference_repository=mock_preference_repository, kafka_producer=mock_kafka_producer
    )

    test_preference = Preference(
        profile_id=123,
        gender=Gender.male,
        age=30,
        radius=100,
    )
    mock_preference_repository.create_preference.side_effect = PreferenceAlreadyExistsError(
        profile_id=123
    )

    with pytest.raises(PreferenceAlreadyExistsError):
        await service.create_preference(test_preference)

    mock_preference_repository.create_preference.assert_called_once_with(test_preference)


async def test_create_profile_create_error():
    mock_preference_repository = AsyncMock()
    mock_kafka_producer = AsyncMock()
    service = PreferenceService(
        preference_repository=mock_preference_repository, kafka_producer=mock_kafka_producer
    )

    test_preference = Preference(
        profile_id=123,
        gender=Gender.male,
        age=30,
        radius=100,
    )
    mock_preference_repository.create_preference.side_effect = PreferenceCreateError(profile_id=123)

    with pytest.raises(PreferenceCreateError):
        await service.create_preference(test_preference)

    mock_preference_repository.create_preference.assert_called_once_with(test_preference)


async def test_create_preference_kafka_connection_error():
    mock_preference_repository = AsyncMock()
    mock_kafka_producer = AsyncMock()
    service = PreferenceService(
        preference_repository=mock_preference_repository, kafka_producer=mock_kafka_producer
    )

    test_preference = Preference(
        profile_id=123,
        gender=Gender.male,
        age=30,
        radius=100,
    )
    mock_preference_repository.create_preference.side_effect = KafkaConnectionError()

    with pytest.raises(KafkaConnectionError):
        await service.create_preference(test_preference)

    mock_preference_repository.create_preference.assert_called_once_with(test_preference)


async def test_create_preference_empty_preference():
    with pytest.raises(TypeError):
        Preference()  # type: ignore
