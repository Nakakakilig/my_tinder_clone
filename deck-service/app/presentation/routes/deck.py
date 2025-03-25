from fastapi import APIRouter  # , HTTPException

# import app.crud.preference as preference_crud
# import app.crud.profile as profile_crud
# from app.api.deps import db_dependency, deck_dependency
# from app.core.config import settings
# from app.core.schemas.deck import MatchDeck
# from app.core.schemas.preferences import PreferenceBase
# from app.services.profile_client import convert_to_model

router = APIRouter(tags=["decks"])


@router.post("/{profile_id}/refresh")  # , response_model=MatchDeck)
async def generate_deck(profile_id: int):
    return {"message": f"Genarate deck for profile {profile_id}"}


#     session: db_dependency,
#     profile_id: int,
#     cache: deck_dependency,
#     limit: int = settings.deck.limit_matched_profiles,
# ):
#     preferences_model = await preference_crud.get_preference_by_profile_id(
#         session=session, profile_id=profile_id
#     )

#     preferences = PreferenceBase(**preferences_model.__dict__)
#     candidate_profiles = await profile_crud.get_matching_profiles(
#         session, profile_id, preferences, limit=limit
#     )
#     candidates = await convert_to_model(
#         candidate_profiles,
#     )

#     deck = MatchDeck(profile_id=profile_id, candidates=candidates)
#     await cache.set_deck(profile_id, deck.model_dump())

#     return deck


@router.get("/{profile_id}")  # , response_model=MatchDeck)
async def get_deck(profile_id):
    return {"message": f"Deck for profile {profile_id} "}
    # profile_id: int, cache: deck_dependency):
    # deck_data = await cache.get_deck(profile_id)
    # if deck_data is None:
    #     raise HTTPException(
    #         status_code=404, detail="Deck not found. Please generate a deck first."
    #     )

    # deck = MatchDeck(**deck_data)
    # return deck
