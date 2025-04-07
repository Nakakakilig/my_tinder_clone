class SwipeClientError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class SwipeHTTPError(SwipeClientError):
    def __init__(self, status_code: int):
        super().__init__(f"Swipe HTTP error occurred: {status_code}")
        self.status_code = status_code


class SwipeRequestError(SwipeClientError):
    def __init__(self, error_message: str):
        super().__init__(f"Swipe HTTP request failed: {error_message}")


class SwipeUnexpectedError(SwipeClientError):
    def __init__(self, error_message: str):
        super().__init__(f"Swipe unexpected error occurred: {error_message}")
