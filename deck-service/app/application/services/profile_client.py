from application.schemas.deck import MatchCard
from application.schemas.profile import ProfileWithDistance


async def convert_to_model(
    candidate_profiles_dict: list[dict],
) -> list[MatchCard]:
    profiles_with_distance: list[ProfileWithDistance] = [
        ProfileWithDistance(**candidate) for candidate in candidate_profiles_dict
    ]
    candidates = [
        MatchCard(
            profile_id=prof_w_dist.profile.id,
            first_name=prof_w_dist.profile.first_name,
            last_name=prof_w_dist.profile.last_name,
            gender=prof_w_dist.profile.gender.value,
            age=prof_w_dist.profile.age,
            distance_km=prof_w_dist.distance_km,
        )
        for prof_w_dist in profiles_with_distance
    ]
    return candidates
