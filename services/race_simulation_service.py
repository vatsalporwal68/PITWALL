from domain.lap_model import LapModel
from domain.race_state import LapResult, RaceState


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
) -> list[LapResult]:
    lap_results = []

    for _ in range(lap_count):
        _, lap_time = advance_race_state(
            state,
            lap_model,
            fuel_consumption
        )

        lap_results.append(
            LapResult(
                lap_number=state.current_lap,
                lap_time=lap_time,
                tyre_age=state.tyre_age,
                fuel_load=state.fuel_load,
                position=state.position
            )
        )

    return lap_results

def perform_pit_stop(
    state: RaceState,
    new_compound: str
) -> RaceState:
    state.change_tyre(new_compound)
    return state    

def calculate_stint_summary(lap_results):
    if not lap_results:
        return {
            "lap_count": 0,
            "total_time": 0,
            "average_lap_time": None,
            "best_lap_time": None,
            "worst_lap_time": None,
            "fuel_remaining": None,
            "tyre_age": None
        }

    lap_times = [result.lap_time for result in lap_results]

    return {
        "lap_count": len(lap_results),
        "total_time": round(sum(lap_times), 3),
        "average_lap_time": round(sum(lap_times) / len(lap_times), 3),
        "best_lap_time": round(min(lap_times), 3),
        "worst_lap_time": round(max(lap_times), 3),
        "fuel_remaining": lap_results[-1].fuel_load,
        "tyre_age": lap_results[-1].tyre_age
    }       