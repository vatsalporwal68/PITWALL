from domain.lap_model import LapModel
from domain.race_state import RaceState


def advance_race_state(
    state: RaceState,
    lap_model: LapModel
) -> tuple[RaceState, float]:
    state.advance_lap()

    lap_time = lap_model.calculate_lap_time(
        state.tyre_age
    )

    return state, lap_time