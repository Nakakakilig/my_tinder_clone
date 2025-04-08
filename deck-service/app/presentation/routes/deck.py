from typing import Annotated

from fastapi import APIRouter, Depends, status

from config.settings import settings
from domain.models.deck import MatchDeck
from presentation.dependencies.deck import get_deck_service
from use_cases.deck import DeckService

router = APIRouter(tags=["decks"])


@router.get("/", response_model=list[MatchDeck])
async def get_all_decks(
    deck_service: Annotated[DeckService, Depends(get_deck_service)],
):
    return await deck_service.get_all_decks()


@router.get("/{profile_id}")
async def get_deck(
    profile_id: int,
    deck_service: Annotated[DeckService, Depends(get_deck_service)],
) -> MatchDeck:
    return await deck_service.get_deck_by_id(profile_id)


@router.post("/{profile_id}/refresh", status_code=status.HTTP_201_CREATED)
async def generate_deck(
    profile_id: int,
    deck_service: Annotated[DeckService, Depends(get_deck_service)],
    limit: int = settings.deck.limit_matched_profiles,
) -> MatchDeck:
    return await deck_service.generate_deck_by_id(profile_id, limit)


@router.delete("/cache", status_code=status.HTTP_204_NO_CONTENT)
async def clear_all_deck_cache(
    deck_service: Annotated[DeckService, Depends(get_deck_service)],
) -> None:
    await deck_service.clear_all_deck_cache()


@router.delete("/cache/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def clear_deck_cache(
    profile_id: int,
    deck_service: Annotated[DeckService, Depends(get_deck_service)],
) -> None:
    await deck_service.clear_deck_cache_by_id(profile_id)
