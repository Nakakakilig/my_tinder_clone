class DeckNotFoundError(Exception):
    pass


class DeckGenerateError(Exception):
    pass


class CandidateNotFoundError(Exception):
    pass


class DeckCacheError(Exception):
    pass


class DeckCacheClearError(Exception):
    pass


class PreferenceNotFoundError(Exception):
    pass


class PreferenceCreateError(Exception):
    pass


class PreferenceAlreadyExistsError(Exception):
    pass


class ProfileNotFoundError(Exception):
    pass


class ProfileCreateError(Exception):
    pass


class ProfileAlreadyExistsError(Exception):
    pass
