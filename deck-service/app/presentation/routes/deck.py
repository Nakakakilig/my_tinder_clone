from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from application.services.deck import DeckService
from config.settings import settings
from domain.models.deck import MatchDeck
from presentation.dependencies.deck import get_deck_service

router = APIRouter(tags=["decks"])


@router.get("/", response_model=list[MatchDeck])
async def get_all_decks(
    deck_service: Annotated[DeckService, Depends(get_deck_service)],
):
    return await deck_service.get_all_decks()


@router.get("/{profile_id}", response_model=MatchDeck)
async def get_deck(
    profile_id: int,
    deck_service: Annotated[DeckService, Depends(get_deck_service)],
):
    try:
        return await deck_service.get_deck_by_id(profile_id)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{profile_id}/refresh", response_model=MatchDeck)
async def generate_deck(
    profile_id: int,
    deck_service: Annotated[DeckService, Depends(get_deck_service)],
    limit: int = settings.deck.limit_matched_profiles,
):
    try:
        return await deck_service.generate_deck_by_id(profile_id, limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/cache")
async def clear_all_deck_cache(
    deck_service: Annotated[DeckService, Depends(get_deck_service)],
) -> None:
    await deck_service.clear_all_deck_cache()


@router.delete("/cache/{profile_id}")
async def clear_deck_cache(
    profile_id: int,
    deck_service: Annotated[DeckService, Depends(get_deck_service)],
) -> None:
    await deck_service.clear_deck_cache_by_id(profile_id)
