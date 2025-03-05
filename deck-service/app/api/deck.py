from api.deps import deck_dependency
from core.schemas.deck import MatchDeck
from fastapi import APIRouter, HTTPException
from services.deck_logic import generate_deck_logic
from services.preference_client import get_profile_preferences
from services.profile_client import get_candidate_profiles_for_deck
from core.config import settings

router = APIRouter(tags=["decks"])


@router.post("/{profile_id}/refresh", response_model=MatchDeck)
async def generate_deck(
    profile_id: int,
    cache: deck_dependency,
    need_filter: bool = False,
    limit: int = settings.profile_service.limit_matched_profiles,
):
    profile_preferences = await get_profile_preferences(profile_id)
    deck_cards = await get_candidate_profiles_for_deck(
        profile_preferences,
        need_filter=need_filter,
        limit=limit,
    )
    deck = MatchDeck(profile_id=profile_id, candidates=deck_cards)
    return deck
    if not profile_preferences:
        raise HTTPException(status_code=404, detail="Profile not found")

    deck_cards = generate_deck_logic(
        profile_id,
    )

    await cache.set_deck(profile_id, deck.dict())

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
