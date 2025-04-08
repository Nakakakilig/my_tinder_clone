from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from config.settings import settings
from domain.exceptions import (
    DeckCacheClearError,
    DeckCacheError,
    DeckGenerateError,
    DeckNotFoundError,
)
from domain.models.deck import MatchDeck
from presentation.dependencies.deck import get_deck_service
from use_cases.deck import DeckService

router = APIRouter(tags=["decks"])


@router.get("/", response_model=list[MatchDeck])
async def get_all_decks(
    deck_service: Annotated[DeckService, Depends(get_deck_service)],
):
    try:
        return await deck_service.get_all_decks()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.get("/{profile_id}")
async def get_deck(
    profile_id: int,
    deck_service: Annotated[DeckService, Depends(get_deck_service)],
) -> MatchDeck:
    try:
        return await deck_service.get_deck_by_id(profile_id)
    except DeckNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post("/{profile_id}/refresh", status_code=status.HTTP_201_CREATED)
async def generate_deck(
    profile_id: int,
    deck_service: Annotated[DeckService, Depends(get_deck_service)],
    limit: int = settings.deck.limit_matched_profiles,
) -> MatchDeck:
    try:
        return await deck_service.generate_deck_by_id(profile_id, limit)

    except DeckGenerateError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to generate deck: " + str(e)
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred: " + str(e),
        ) from e


@router.delete("/cache", status_code=status.HTTP_204_NO_CONTENT)
async def clear_all_deck_cache(
    deck_service: Annotated[DeckService, Depends(get_deck_service)],
) -> None:
    try:
        await deck_service.clear_all_deck_cache()
    except DeckCacheError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear all deck cache: {e!s}",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while clearing all deck cache: {e!s}",
        ) from e


@router.delete("/cache/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def clear_deck_cache(
    profile_id: int,
    deck_service: Annotated[DeckService, Depends(get_deck_service)],
) -> None:
    try:
        await deck_service.clear_deck_cache_by_id(profile_id)
    except DeckCacheClearError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear deck cache for profile {profile_id}: {e!s}",
        ) from e
    except DeckNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deck not found for profile {profile_id}: {e!s}",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while clearing deck cache: {e!s}",
        ) from e
