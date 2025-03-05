import httpx
from core.config import settings

from common.preferences import PreferenceBase
from common.profile import ProfileRead, ProfileWithDistance

from core.schemas.deck import MatchCard


async def get_candidate_profiles_for_deck(
    preferences: PreferenceBase,
    need_filter: bool,
    limit: int,
) -> list[MatchCard]:
    params = {
        "gender": preferences.gender.value,
        "age": preferences.age,
        "radius": preferences.radius,
        "limit": limit,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            settings.profile_service.get_matching_profiles_url(preferences.profile_id),
            params=params if need_filter else None,
        )
        response.raise_for_status()
        response_json: ProfileWithDistance = response.json()
    profiles: list[ProfileRead] = [
        ProfileRead(**candidate["profile"]) for candidate in response_json
    ]
    distances: list[float] = [candidate["distance_km"] for candidate in response_json]

    res = []
    for profile, distance in zip(profiles, distances):
        card = MatchCard(
            profile_id=profile.id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            gender=profile.gender.value,
            age=profile.age,
            distance_km=distance,
        )
        res.append(card)
    return res
