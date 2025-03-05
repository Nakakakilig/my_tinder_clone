from fastapi import HTTPException
import httpx
from core.config import settings

from core.schemas.preferences import PreferenceBase


async def get_profile_preferences(profile_id: int) -> PreferenceBase:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                settings.preference_service.get_preference_url(profile_id)
            )
            response.raise_for_status()
            preference = response.json()
        return PreferenceBase(**preference)

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Preference not found")
        raise HTTPException(status_code=500, detail="Error while getting preferences")

    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Profile-service is unavailable")
