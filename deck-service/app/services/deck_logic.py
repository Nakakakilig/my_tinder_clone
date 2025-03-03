import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)  # for common
from common.preferences import PreferenceRead


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
