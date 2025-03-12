import httpx
from app.core.config import settings
from app.core.schemas.deck import MatchCard
from app.core.schemas.preferences import PreferenceBase
from app.core.schemas.profile import ProfileWithDistance
from fastapi import HTTPException


async def get_candidate_profiles(
    preferences: PreferenceBase,
    need_filter: bool,
    limit: int,
) -> list | dict:
    params = {
        "gender": preferences.gender.value,
        "age": preferences.age,
        "radius": preferences.radius,
        "limit": limit,
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                settings.profile_service.get_matching_profiles_url(
                    preferences.profile_id
                ),
                params=params if need_filter else None,
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(
                    status_code=500,
                    detail="Matching profiles not found. Change preferences!",
                )

            raise HTTPException(
                status_code=500, detail="Error while getting preferences"
            )

        except httpx.RequestError:
            raise HTTPException(
                status_code=503, detail="Profile-service is unavailable"
            )


async def convert_to_model(
    candidate_profiles_dict: list[dict],
) -> list[MatchCard]:
    profiles_with_distance: list[ProfileWithDistance] = [
        ProfileWithDistance(**candidate) for candidate in candidate_profiles_dict
    ]
    candidates = [
        MatchCard(
            profile_id=prof_w_dist.profile.id,
            first_name=prof_w_dist.profile.first_name,
            last_name=prof_w_dist.profile.last_name,
            gender=prof_w_dist.profile.gender.value,
            age=prof_w_dist.profile.age,
            distance_km=prof_w_dist.distance_km,
        )
        for prof_w_dist in profiles_with_distance
    ]
    return candidates
