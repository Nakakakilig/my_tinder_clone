from api.deps import deck_dependency
from core.schemas.deck import DeckRead
from fastapi import APIRouter, HTTPException
from services.deck_logic import generate_deck_logic
from services.preference_client import get_profile_preferences
from services.profile_client import get_candidate_profiles_for_deck

router = APIRouter(tags=["deck"])


@router.post("/generate/{profile_id}", response_model=DeckRead)
async def generate_deck(profile_id: int, cache: deck_dependency):
    profile_preferences = await get_profile_preferences(profile_id)
    print(f"{profile_preferences = }")
    candidate_profiles = await get_candidate_profiles_for_deck(profile_preferences)
    candidate_profiles
    return
    if not profile_preferences:
        raise HTTPException(status_code=404, detail="Profile not found")

    deck_cards = generate_deck_logic(
        profile_id,
    )
    deck = DeckRead(profile_id=profile_id, cards=deck_cards)

    await cache.set_deck(profile_id, deck.dict())

    return deck


@router.get("/{profile_id}", response_model=DeckRead)
async def get_deck(profile_id: int, cache: deck_dependency):
    deck_data = await cache.get_deck(profile_id)
    if deck_data is None:
        raise HTTPException(
            status_code=404, detail="Deck not found. Please generate a deck first."
        )

    deck = DeckRead(**deck_data)
    return deck
