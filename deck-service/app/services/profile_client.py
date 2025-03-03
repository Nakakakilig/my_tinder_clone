import httpx
from core.config import settings

from common.preferences import PreferenceBase
from common.profile import ProfileRead


async def get_candidate_profiles_for_deck(
    preferences: PreferenceBase,
) -> list[ProfileRead]:
    # TODO: add filter (better filter in Select, then in backend)

    async with httpx.AsyncClient() as client:
        # TODO: change get_all_profiles_url to 'get candidates that match with preferences'
        response = await client.get(settings.profile_service.get)
        response.raise_for_status()
        profiles = response.json()
    profiles = [ProfileRead(**profile) for profile in profiles]
    return profiles
