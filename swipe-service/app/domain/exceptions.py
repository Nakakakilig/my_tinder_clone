class SwipeAlreadyExistsError(Exception):
    def __init__(self, profile_id_1: int, profile_id_2: int):
        super().__init__(f"Swipe already exists for profiles {profile_id_1} and {profile_id_2}")


class SwipeCreateError(Exception):
    def __init__(self, profile_id_1: int, profile_id_2: int):
        super().__init__(f"Error creating swipe for profiles {profile_id_1} and {profile_id_2}")


class SwipeNotFoundError(Exception):
    def __init__(self, profile_id_1: int | None = None, profile_id_2: int | None = None):
        if profile_id_1 and not profile_id_2:
            super().__init__(f"Swipes for {profile_id_1} not found")
        elif profile_id_1 and profile_id_2:
            if profile_id_1 == profile_id_2:
                super().__init__(
                    "Profile_1 ID cannot be the same as Profile_2 ID. Please check the input data."
                )
            else:
                super().__init__(f"Swipes for profiles {profile_id_1} and {profile_id_2} not found")
        else:
            super().__init__("Swipes not found")
