import httpx
from core.config import settings

from common.preferences import PreferenceBase


async def get_profile_preferences(profile_id: int) -> PreferenceBase:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            settings.preference_service.get_preference_url(profile_id)
        )
        response.raise_for_status()
        profile = response.json()
    profile = PreferenceBase(**profile)
    return profile
