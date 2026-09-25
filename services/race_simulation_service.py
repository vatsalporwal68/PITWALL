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

def simulate_laps(
    state: RaceState,
    lap_model: LapModel,
    fuel_consumption: float,
    lap_count: int
) -> list[float]:
    lap_times = []

    for _ in range(lap_count):
        _, lap_time = advance_race_state(
            state,
            lap_model,
            fuel_consumption
        )

        lap_times.append(lap_time)

    return lap_times    