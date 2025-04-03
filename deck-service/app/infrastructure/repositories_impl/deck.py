from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import settings
from domain.exceptions import (
    CandidateNotFoundError,
    DeckCacheError,
    DeckGenerateError,
    PreferenceNotFoundError,
    ProfileNotFoundError,
)
from domain.models.deck import MatchCard, MatchDeck
from domain.repositories.cache import ICache
from domain.repositories.deck import IDeckRepository
from infrastructure.db.db_models import ProfileORM
from utils.calc_distance import calc_distance_in_query


class DeckRepositoryImpl(IDeckRepository):
    def __init__(self, db_session: AsyncSession, cache: ICache):
        self.db_session = db_session
        self.cache = cache

    async def get_deck_by_id(self, profile_id: int) -> MatchDeck:
        deck_data = await self.cache.get(f"deck:{profile_id}")
        if not deck_data:
            raise Exception(f"Deck for profile {profile_id} not found in cache")
        return MatchDeck(**deck_data)

    async def generate_deck_by_id(self, profile_id: int, limit: int):
        try:
            profiles_and_distance = await self._get_matching_profiles_and_distance(
                profile_id, limit
            )
            cards: list[MatchCard] = await self._convert_to_cards(profiles_and_distance)
            deck = MatchDeck(profile_id=profile_id, candidates=cards)
            await self.cache.set(f"deck:{profile_id}", deck.model_dump())
            return deck

        except CandidateNotFoundError as e:
            raise CandidateNotFoundError(
                f"Error generating deck: No candidates found for profile {profile_id}"
            ) from e
        except ProfileNotFoundError as e:
            raise ProfileNotFoundError(
                f"Error generating deck: Profile {profile_id} not found"
            ) from e
        except PreferenceNotFoundError as e:
            raise PreferenceNotFoundError(
                f"Error generating deck: Preference not found for profile {profile_id}"
            ) from e
        except DeckCacheError as e:
            raise DeckCacheError(
                f"Error generating deck: Cant save deck to cache for profile {profile_id}"
            ) from e
        except Exception as e:
            raise DeckGenerateError(f"Error generating deck: {e}") from e

    async def clear_deck_cache_by_id(self, profile_id: int) -> None:
        await self.cache.delete(f"deck:{profile_id}")
        return

    async def get_all_decks(self) -> list[MatchDeck]:
        decks_data = await self.cache.get_all_values()
        if not decks_data:
            raise Exception("No decks found in cache")
        decks = [MatchDeck(**deck_data) for deck_data in decks_data]
        sorted_decks = sorted(decks, key=lambda x: x.profile_id)
        return sorted_decks

    async def clear_all_deck_cache(self) -> None:
        await self.cache.clear()
        return

    async def _get_matching_profiles_and_distance(
        self, profile_id: int, limit: int
    ) -> list[tuple[ProfileORM, float]]:
        result = await self.db_session.execute(
            select(ProfileORM).where(ProfileORM.id == profile_id)
        )
        profile = result.scalars().first()

        if not profile:
            raise ProfileNotFoundError("Profile not found")

        preference = profile.preference
        if not preference:
            raise PreferenceNotFoundError("Preference not found")
        distance_expr = calc_distance_in_query(profile, ProfileORM)  # type: ignore

        filters = [
            ProfileORM.gender == preference.gender,
            ProfileORM.age >= preference.age - settings.deck.age_range,
            ProfileORM.age <= preference.age + settings.deck.age_range,
        ]
        query = (
            select(ProfileORM, distance_expr)
            .filter(and_(*filters))
            .group_by(ProfileORM.id)
            .order_by(distance_expr)
            .limit(limit)
        )

        query = query.having(distance_expr <= preference.radius)

        result = await self.db_session.execute(query)
        profiles_and_distance: list[tuple[ProfileORM, float]] = result.all()  # type: ignore
        return profiles_and_distance

    async def _convert_to_cards(
        self, profile_and_distance: list[tuple[ProfileORM, float]]
    ) -> list[MatchCard]:
        cards: list[MatchCard] = []
        for profile, distance in profile_and_distance:
            card = MatchCard(distance_km=distance, profile_id=profile.id, **profile.__dict__)
            cards.append(card)
        return cards
