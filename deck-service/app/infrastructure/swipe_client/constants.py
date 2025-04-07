from config.settings import settings

SWIPE_API_PATHS = {
    "get_profile_swipes": settings.swipe.get_profile_swipes,
    "get_swipe_by_profiles": settings.swipe.get_swipe_by_profiles,
}
