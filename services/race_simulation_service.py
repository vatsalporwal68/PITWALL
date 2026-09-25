from domain.lap_model import LapModel
from domain.race_state import (
    LapResult,
    RaceState,
    StrategyResult,
    StrategyComparisonResult
)


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
    new_compound: str,
    pit_stop_time: float
) -> tuple[RaceState, float]:
    state.change_tyre(new_compound)

    return state, pit_stop_time   

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

def simulate_strategy(
    strategy_name: str,
    state: RaceState,
    lap_model: LapModel,
    stints: list[dict],
    fuel_consumption: float,
    pit_stop_time: float
) -> StrategyResult:
    total_race_time = 0.0
    pit_stops = 0

    for stint in stints:
        lap_results = simulate_laps(
            state,
            lap_model,
            fuel_consumption,
            stint["lap_count"]
        )

        summary = calculate_stint_summary(lap_results)

        total_race_time += summary["total_time"]

        if stint != stints[-1]:
            _, pit_time = perform_pit_stop(
                state,
                stint["next_compound"],
                pit_stop_time
            )

            total_race_time += pit_time
            pit_stops += 1

    return StrategyResult(
        strategy_name=strategy_name,
        total_race_time=round(total_race_time, 3),
        pit_stops=pit_stops
    )

def compare_strategies(
    strategy_results: list[StrategyResult]
) -> StrategyComparisonResult:
    return StrategyComparisonResult(
        strategies=strategy_results
    )              