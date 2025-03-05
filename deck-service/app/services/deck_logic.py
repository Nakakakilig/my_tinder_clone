from core.schemas.preferences import PreferenceRead


def generate_deck_logic(
    profile_id: int, candidate_profiles: list[PreferenceRead]
) -> list[dict[str, int | str | float]]:
    deck = []
    for profile in candidate_profiles:
        if profile.id == profile_id:
            continue

        deck.append(profile.model_dump())

    deck.sort(key=lambda x: x["id"])
    return deck
