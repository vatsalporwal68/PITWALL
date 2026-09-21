from domain.lap_model import LapModel
from domain.race_state import RaceState


def advance_race_state(
    state: RaceState,
    lap_model: LapModel,
    fuel_consumption: float
) -> tuple[RaceState, float]:
    state.advance_lap()

    lap_time = lap_model.calculate_lap_time(
        tyre_age=state.tyre_age,
        fuel_load=state.fuel_load
    )

    state.fuel_load -= fuel_consumption

    return state, lap_time