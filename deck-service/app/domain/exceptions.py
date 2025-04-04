class DeckNotFoundError(Exception):
    def __init__(self, profile_id: int | None = None):
        if profile_id:
            super().__init__(f"Deck for profile {profile_id} not found")
        else:
            super().__init__("Deck not found")


class DeckGenerateError(Exception):
    def __init__(self, profile_id: int):
        super().__init__(f"Deck generation for profile {profile_id} failed")


class CandidateNotFoundError(Exception):
    def __init__(self, profile_id: int):
        super().__init__(f"Candidate for profile {profile_id} not found")


class DeckCacheError(Exception):
    def __init__(self, profile_id: int | None = None):
        if profile_id:
            super().__init__(f"Deck cache for profile {profile_id} error")
        else:
            super().__init__("Deck cache error")


class DeckCacheClearError(Exception):
    def __init__(self, profile_id: int | None = None):
        if profile_id:
            super().__init__(f"Deck cache for profile {profile_id} clear failed")
        else:
            super().__init__("Deck cache clear error")


class PreferenceNotFoundError(Exception):
    def __init__(self, preference_id: int | None = None):
        self.preference_id = preference_id
        if preference_id is not None:
            super().__init__(f"Preference {preference_id} not found")
        else:
            super().__init__("Preference not found")


class PreferenceForProfileNotFoundError(PreferenceNotFoundError):
    def __init__(self, profile_id: int):
        self.profile_id = profile_id
        message = f"Preference for profile {profile_id} not found"
        super().__init__(None)
        self.args = (message,)  # copy paste from internet


class PreferenceCreateError(Exception):
    def __init__(self):
        super().__init__("Preference creation error")


class PreferenceAlreadyExistsError(Exception):
    def __init__(self, preference_id: int | None = None):
        if preference_id:
            super().__init__(f"Preference {preference_id} already exists")
        else:
            super().__init__("Preference already exists")


class ProfileNotFoundError(Exception):
    def __init__(self, profile_id: int | None = None):
        if profile_id:
            super().__init__(f"Profile {profile_id} not found")
        else:
            super().__init__("Profile not found")


class ProfileCreateError(Exception):
    def __init__(self):
        super().__init__("Profile creation failed")


class ProfileAlreadyExistsError(Exception):
    def __init__(self, profile_id: int):
        super().__init__(f"Profile {profile_id} already exists")
