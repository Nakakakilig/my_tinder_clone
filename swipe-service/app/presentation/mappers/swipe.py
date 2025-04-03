from application.schemas.swipe import SwipeReadSchema
from domain.models.swipe import Swipe


def swipe_to_read_schema(swipe: Swipe) -> SwipeReadSchema:
    return SwipeReadSchema.model_validate(swipe.__dict__)


def swipes_to_read_schema_list(swipes: list[Swipe]) -> list[SwipeReadSchema]:
    return [swipe_to_read_schema(s) for s in swipes]
