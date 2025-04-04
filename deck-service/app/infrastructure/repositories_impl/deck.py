from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import settings
from domain.exceptions import (
    CandidateNotFoundError,
    DeckCacheError,
    DeckGenerateError,
    PreferenceForProfileNotFoundError,
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
            raise DeckCacheError(profile_id)
        return MatchDeck(**deck_data)

    async def generate_deck_by_id(self, profile_id: int, limit: int):
        try:
            profiles_and_distance = await self._get_matching_profiles_and_distance(
                profile_id, limit
            )
            cards: list[MatchCard] = await self._convert_to_cards(profiles_and_distance)
            deck = MatchDeck(profile_id=profile_id, candidates=cards)
            await self.cache.set(f"deck:{profile_id}", deck.model_dump())
            return deck  # noqa: TRY300

        except CandidateNotFoundError as e:
            raise CandidateNotFoundError(profile_id) from e
        except ProfileNotFoundError as e:
            raise ProfileNotFoundError(profile_id) from e
        except PreferenceNotFoundError as e:
            raise PreferenceNotFoundError(profile_id) from e
        except DeckCacheError as e:
            raise DeckCacheError(profile_id) from e
        except Exception as e:
            raise DeckGenerateError(profile_id) from e

    async def clear_deck_cache_by_id(self, profile_id: int) -> None:
        await self.cache.delete(f"deck:{profile_id}")
        return  # noqa: PLR1711

    async def get_all_decks(self) -> list[MatchDeck]:
        decks_data = await self.cache.get_all_values()
        if not decks_data:
            raise DeckCacheError()
        decks = [MatchDeck(**deck_data) for deck_data in decks_data]
        sorted_decks = sorted(decks, key=lambda x: x.profile_id)
        return sorted_decks  # noqa: RET504

    async def clear_all_deck_cache(self) -> None:
        await self.cache.clear()
        return  # noqa: PLR1711

    async def _get_matching_profiles_and_distance(
        self, profile_id: int, limit: int
    ) -> list[tuple[ProfileORM, float]]:
        result = await self.db_session.execute(
            select(ProfileORM).where(ProfileORM.id == profile_id)
        )
        profile = result.scalars().first()

        if not profile:
            raise ProfileNotFoundError(profile_id)

        preference = profile.preference
        if not preference:
            raise PreferenceForProfileNotFoundError(profile_id)
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
