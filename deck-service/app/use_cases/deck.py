from domain.exceptions import (
    CandidateNotFoundError,
    DeckCacheError,
    DeckGenerateError,
    ProfileNotFoundError,
)
from domain.models.deck import MatchCard, MatchDeck
from domain.repositories.deck import IDeckRepository
from domain.repositories.profile import IProfileRepository
from domain.repositories.swipe import ISwipeRepository
from presentation.schemas.profile import ProfileWithDistance  # bad idea!!!


class DeckService:
    def __init__(
        self,
        deck_repository: IDeckRepository,
        profile_repository: IProfileRepository,
        swipe_client: ISwipeRepository,
    ):
        self.deck_repository = deck_repository
        self.profile_repository = profile_repository
        self.swipe_client = swipe_client

    async def get_deck_by_id(self, profile_id: int) -> MatchDeck:
        deck = await self.deck_repository.get_deck_by_id(profile_id)
        if not deck:
            raise DeckCacheError(profile_id)
        return deck

    async def generate_deck_by_id(self, profile_id: int, limit: int) -> MatchDeck:
        try:
            if not profile_id:
                raise ProfileNotFoundError(profile_id)

            candidates_and_distance = await self.profile_repository.get_candidates_and_distance(
                profile_id, limit
            )
            if not candidates_and_distance:
                raise CandidateNotFoundError(profile_id)

            profiles_with_distance = [
                ProfileWithDistance(**candidate.__dict__, distance_km=distance)
                for candidate, distance in candidates_and_distance
            ]

            candidates = await self._filter_profiles_by_swipe(profile_id, profiles_with_distance)

            deck = MatchDeck(
                profile_id=profile_id,
                candidates=[
                    MatchCard(profile_id=candidate.id, **candidate.__dict__)
                    for candidate in candidates
                ],
            )

            await self.deck_repository.save_deck(deck)
            return deck  # noqa: TRY300

        except DeckCacheError as e:
            raise DeckCacheError(profile_id) from e
        except Exception as e:
            raise DeckGenerateError(profile_id, str(e)) from e

    async def get_all_decks(self, limit: int, offset: int) -> list[MatchDeck]:
        return await self.deck_repository.get_all_decks(limit, offset)

    async def clear_deck_cache_by_id(self, profile_id: int) -> None:
        return await self.deck_repository.clear_deck_cache_by_id(profile_id)

    async def clear_all_deck_cache(self) -> None:
        return await self.deck_repository.clear_all_deck_cache()

    async def _filter_profiles_by_swipe(
        self,
        profile_id: int,
        profiles_with_distance: list[ProfileWithDistance],
    ) -> list[ProfileWithDistance]:
        candidates: list[ProfileWithDistance] = []
        for candidate in profiles_with_distance:
            swipe = await self.swipe_client.get_swipe_by_two_profile_ids(candidate.id, profile_id)
            if not swipe:
                # profile_id has not swiped on candidate
                candidates.append(candidate)
            elif (profile_id == swipe.profile_id_1 and not swipe.decision_1) or (
                profile_id == swipe.profile_id_2 and not swipe.decision_2
            ):
                # profile_id has not liked candidate
                candidates.append(candidate)
        return candidates
