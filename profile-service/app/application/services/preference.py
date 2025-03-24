from datetime import datetime

from application.schemas.preference import PreferenceCreateSchema
from config.settings import settings
from domain.models.preference import Preference
from domain.repositories.preference import IPreferenceRepository
from infrastructure.kafka.producer import KafkaProducer


class PreferenceService:
    def __init__(
        self,
        preference_repository: IPreferenceRepository,
        kafka_producer: KafkaProducer,
    ):
        self.preference_repository = preference_repository
        self.kafka_producer = kafka_producer

    async def create_preference(self, preference: Preference) -> Preference:
        preference = await self.preference_repository.create_preference(preference)
        preference_data = PreferenceCreateSchema.model_validate(
            preference.__dict__
        ).model_dump()

        event = {
            "event_type": "preference_created",
            "data": preference_data,
            "timestamp": datetime.now().isoformat(),
        }
        await self.kafka_producer.send_event(settings.kafka.profile_topic, event)
        return preference

    async def get_preference_by_id(self, preference_id: int) -> Preference:
        return await self.preference_repository.get_preference_by_id(preference_id)

    async def get_preference_by_profile_id(self, profile_id: int) -> Preference:
        return await self.preference_repository.get_preference_by_profile_id(profile_id)

    async def get_preferences(self) -> list[Preference]:
        return await self.preference_repository.get_preferences()
