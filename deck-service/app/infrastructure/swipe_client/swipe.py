import httpx

from domain.repositories.swipe import ISwipeRepository, Swipe
from infrastructure.swipe_client.constants import SWIPE_API_PATHS
from infrastructure.swipe_client.exceptions import (
    SwipeHTTPError,
    SwipeRequestError,
    SwipeUnexpectedError,
)


class SwipeClient(ISwipeRepository):
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_swipes_for_profile(self, profile_id: int) -> list[Swipe] | None:
        # todo: not the best way to generate url here because api path can be changed
        # todo: add pagination
        url = (
            f"{self.base_url}{SWIPE_API_PATHS['get_profile_swipes'].format(profile_id=profile_id)}"
        )
        swipe_response = await self._request(url)
        if not swipe_response:
            return None
        return [
            Swipe(
                profile_id_1=response["profile_id_1"],
                profile_id_2=response["profile_id_2"],
                decision_1=response["decision_1"],
                decision_2=response["decision_2"],
            )
            for response in swipe_response
        ]

    async def get_swipe_by_two_profile_ids(
        self, profile_id_1: int, profile_id_2: int
    ) -> Swipe | None:
        # todo: not the best way to generate url here because api path can be changed
        # todo: 'format' looks awful here
        url = f"{self.base_url}" + SWIPE_API_PATHS["get_swipe_by_profiles"].format(
            profile_id_1=profile_id_1, profile_id_2=profile_id_2
        )
        swipe_response = await self._request(url)
        if not swipe_response:
            return None
        return Swipe(
            profile_id_1=swipe_response["profile_id_1"],
            profile_id_2=swipe_response["profile_id_2"],
            decision_1=swipe_response["decision_1"],
            decision_2=swipe_response["decision_2"],
        )

    @staticmethod
    async def _request(url: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()

        except httpx.HTTPStatusError as e:
            raise SwipeHTTPError(e.response.status_code) from e
        except httpx.RequestError as e:
            raise SwipeRequestError(str(e)) from e
        except Exception as e:
            raise SwipeUnexpectedError(str(e)) from e
