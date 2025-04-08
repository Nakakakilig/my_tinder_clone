class UserAlreadyExistsError(Exception):
    def __init__(self, username: str):
        super().__init__(f"User {username} already exists")


class UserCreateError(Exception):
    def __init__(self, username: str):
        super().__init__(f"Error creating user {username}")


class UserNotFoundError(Exception):
    def __init__(self, user_id: int | None = None):
        if user_id:
            super().__init__(f"User {user_id} not found")
        else:
            super().__init__("Users not found")


class ProfileAlreadyExistsError(Exception):
    def __init__(self, user_id: int):
        super().__init__(f"Profile for user {user_id} already exists")


class ProfileCreateError(Exception):
    def __init__(self, user_id: int):
        super().__init__(f"Error creating profile for user {user_id}")


class ProfileNotFoundError(Exception):
    def __init__(self, profile_id: int | None = None, user_id: int | None = None):
        if profile_id:
            super().__init__(f"Profile {profile_id} not found")
        elif user_id:
            super().__init__(f"Profile for user {user_id} not found")
        else:
            super().__init__("Profiles not found")


class PreferenceAlreadyExistsError(Exception):
    def __init__(self, profile_id: int):
        super().__init__(f"Preference for profile {profile_id} already exists")


class PreferenceCreateError(Exception):
    def __init__(self, profile_id: int):
        super().__init__(f"Error creating preference for profile {profile_id}")


class PreferenceNotFoundError(Exception):
    def __init__(self, preference_id: int | None = None, profile_id: int | None = None):
        if preference_id:
            super().__init__(f"Preference {preference_id} not found")
        elif profile_id:
            super().__init__(f"Preference for profile {profile_id} not found")
        else:
            super().__init__("Preferences not found")
