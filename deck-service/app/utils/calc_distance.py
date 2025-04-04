from typing import TYPE_CHECKING

from sqlalchemy import Numeric, cast, func

if TYPE_CHECKING:
    from infrastructure.db.db_models import ProfileORM


def calc_distance_in_query(current_profile: "ProfileORM", profile_orm: "ProfileORM"):
    # TODO: add PostGis instead of raw SQL
    distance_expr = func.round(
        cast(
            6371  # radius of the earth in km
            * func.acos(
                func.cos(func.radians(current_profile.geo_latitude))
                * func.cos(func.radians(profile_orm.geo_latitude))
                * func.cos(
                    func.radians(profile_orm.geo_longitude)
                    - func.radians(current_profile.geo_longitude),
                )
                + func.sin(func.radians(current_profile.geo_latitude))
                * func.sin(func.radians(profile_orm.geo_latitude)),
            ),
            Numeric,
        ),
        2,  # round 2 decimal places
    ).label("distance_km")

    return distance_expr  # noqa: RET504
