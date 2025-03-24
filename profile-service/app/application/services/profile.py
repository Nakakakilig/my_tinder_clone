from datetime import datetime

from application.schemas.profile import ProfileBaseSchema, ProfileCreatedEvent
from domain.models.profile import Profile
from domain.repositories.profile import IProfileRepository
from infrastructure.kafka.producer import KafkaProducer
from config.settings import settings


class ProfileService:
    def __init__(
        self,
        profile_repository: IProfileRepository,
        kafka_producer: KafkaProducer,
    ):
        self.profile_repository = profile_repository
        self.kafka_producer = kafka_producer

    async def create_profile(self, profile: Profile) -> Profile:
        profile = await self.profile_repository.create_profile(profile)
        event = ProfileCreatedEvent(
            **ProfileBaseSchema.model_validate(profile.__dict__).model_dump(),
            occurred_at=datetime.now(),
        )
        await self.kafka_producer.send_event(settings.kafka.profile_topic, event)
        return profile

    async def get_profile_by_id(self, profile_id: int) -> Profile:
        return await self.profile_repository.get_profile_by_id(profile_id)

    async def get_profile_by_user_id(self, user_id: int) -> Profile:
        return await self.profile_repository.get_profile_by_user_id(user_id)

    async def get_profiles(self) -> list[Profile]:
        return await self.profile_repository.get_profiles()
