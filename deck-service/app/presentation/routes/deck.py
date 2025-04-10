from typing import Annotated

import logging
from fastapi import APIRouter, Depends, Path, Query, status

from config.settings import settings
from domain.models.deck import MatchDeck
from presentation.dependencies.deck import get_deck_service
from presentation.routes.common import PaginationParams
from use_cases.deck import DeckService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["decks"])


@router.get("/", response_model=list[MatchDeck])
async def get_all_decks(
    pagination: Annotated[PaginationParams, Depends()],
    deck_service: Annotated[DeckService, Depends(get_deck_service)],
):
    logger.info(
        "Incoming request: get_all_decks (limit=%d, offset=%d)",
        pagination.limit,
        pagination.offset,
    )
    decks = await deck_service.get_all_decks(pagination.limit, pagination.offset)
    logger.info("Returning %d decks", len(decks))
    return decks


@router.get("/{profile_id}")
async def get_deck(
    profile_id: Annotated[int, Path(gt=0)],
    deck_service: Annotated[DeckService, Depends(get_deck_service)],
) -> MatchDeck:
    logger.info("Incoming request: get_deck (profile_id=%d)", profile_id)
    deck = await deck_service.get_deck_by_id(profile_id)
    logger.info("Returning deck for profile_id %d", profile_id)
    return deck


@router.post("/{profile_id}/refresh", status_code=status.HTTP_201_CREATED)
async def generate_deck(
    profile_id: Annotated[int, Path(gt=0)],
    deck_service: Annotated[DeckService, Depends(get_deck_service)],
    limit: Annotated[
        int,
        Query(ge=settings.pagination.min_limit, le=settings.pagination.max_limit),
    ] = settings.pagination.default_limit,
) -> MatchDeck:
    logger.info(
        "Incoming request: generate_deck (profile_id=%d, limit=%d)",
        profile_id,
        limit,
    )
    deck = await deck_service.generate_deck_by_id(profile_id, limit)
    logger.info("Returning deck for profile_id %d", profile_id)
    return deck


@router.delete("/cache", status_code=status.HTTP_204_NO_CONTENT)
async def clear_all_deck_cache(
    deck_service: Annotated[DeckService, Depends(get_deck_service)],
) -> None:
    logger.info("Incoming request: clear_all_deck_cache")
    await deck_service.clear_all_deck_cache()
    logger.info("Cleared all deck cache")


@router.delete("/cache/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def clear_deck_cache(
    profile_id: Annotated[int, Path(gt=0)],
    deck_service: Annotated[DeckService, Depends(get_deck_service)],
) -> None:
    logger.info("Incoming request: clear_deck_cache (profile_id=%d)", profile_id)
    await deck_service.clear_deck_cache_by_id(profile_id)
    logger.info("Cleared deck cache for profile_id %d", profile_id)
