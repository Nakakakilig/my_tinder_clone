from domain.models.swipe import Swipe
from infrastructure.db.db_models import SwipeORM


def orm_to_domain(swipe_orm: SwipeORM) -> Swipe:
    return Swipe(
        **{
            key: value
            for key, value in swipe_orm.__dict__.items()
            if key in Swipe.__annotations__
        }
    )


def domain_to_orm(swipe: Swipe) -> SwipeORM:
    return SwipeORM(**swipe.__dict__)
