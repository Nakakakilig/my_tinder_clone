import asyncio
import random

import app.crud.swipe as swipe_crud
from app.core.db.db_helper import db_helper
from app.core.schemas.swipe import SwipeCreate


async def create_swipes_between_profiles(N_profiles: int = 100):
    swipe_creates = []

    decisions = {i: {} for i in range(1, N_profiles + 1)}

    for i in range(1, N_profiles + 1):  # for each profile
        # Choose random profiles for swipes, excluding the current profile
        other_profiles = [x for x in range(1, N_profiles + 1) if x != i]
        # choose random number of swipes
        num_swipes = random.randint(2, len(other_profiles))
        # choose random profiles for swipes
        selected_profiles = random.sample(other_profiles, num_swipes)

        for j in selected_profiles:
            # if profile_i likes profile_j, write decision_1
            decision_1 = random.choice([True, False])
            decisions[i][j] = decision_1

            # if profile_j likes profile_i, check if profile_i likes profile_j
            decision_2 = None
            if j in decisions and i in decisions[j] and decisions[j][i] is not None:
                # if there is a like from j to i, then decision_2 will depend on the decision of j
                decision_2 = random.choice([True, False])

            # if profile_j likes profile_i and decision_2 is defined, add this record
            if decision_2 is not None:
                swipe_creates.append(
                    SwipeCreate(
                        profile_id_1=i,
                        profile_id_2=j,
                        decision_1=decision_1,
                        decision_2=decision_2,
                    )
                )
            # if only decision_1 is set, add only it
            else:
                swipe_creates.append(
                    SwipeCreate(
                        profile_id_1=i,
                        profile_id_2=j,
                        decision_1=decision_1,
                    )
                )

    await asyncio.sleep(5)

    async for session in db_helper.session_getter():
        for swipe_create in swipe_creates:
            await swipe_crud.create_swipe(session, swipe_create)

    print(f"Created {len(swipe_creates)} swipes")
