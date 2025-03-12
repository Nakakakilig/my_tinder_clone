from fastapi import APIRouter, HTTPException

from app.api.deps import deck_dependency
from app.core.config import settings
from app.core.schemas.deck import MatchDeck
from app.services.preference_client import get_profile_preferences
from app.services.profile_client import convert_to_model, get_candidate_profiles

router = APIRouter(tags=["decks"])


@router.post("/{profile_id}/refresh", response_model=MatchDeck)
async def generate_deck(
    profile_id: int,
    cache: deck_dependency,
    need_filter: bool = False,
    limit: int = settings.profile_service.limit_matched_profiles,
):
    preferences = await get_profile_preferences(profile_id)
    candidate_profiles = await get_candidate_profiles(
        preferences,
        need_filter=need_filter,
        limit=limit,
    )
    candidates = await convert_to_model(
        candidate_profiles,
    )

    deck = MatchDeck(profile_id=profile_id, candidates=candidates)
    await cache.set_deck(profile_id, deck.model_dump())

    return deck


@router.get("/{profile_id}", response_model=MatchDeck)
async def get_deck(profile_id: int, cache: deck_dependency):
    deck_data = await cache.get_deck(profile_id)
    if deck_data is None:
        raise HTTPException(
            status_code=404, detail="Deck not found. Please generate a deck first."
        )

    deck = MatchDeck(**deck_data)
    return deck
