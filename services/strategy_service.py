from dataclasses import replace
from itertools import product

from domain.lap_model import LapModel
from domain.race_state import RaceState, StrategyResult
from domain.strategy import Strategy
from services.race_simulation_service import simulate_strategy


def generate_strategies(
    race_laps: int,
    compounds: list[str],
    min_stint_laps: int = 2,
    max_stints: int = 3
) -> list[Strategy]:
    strategies = []

    def generate_lengths(
        remaining_laps: int,
        stint_count: int,
        current_lengths: list[int]
    ) -> list[list[int]]:
        if stint_count == 1:
            if remaining_laps >= min_stint_laps:
                return [
                    current_lengths + [remaining_laps]
                ]
            return []

        results = []

        max_length = (
            remaining_laps
            - min_stint_laps * (stint_count - 1)
        )

        for stint_length in range(
            min_stint_laps,
            max_length + 1
        ):
            results.extend(
                generate_lengths(
                    remaining_laps - stint_length,
                    stint_count - 1,
                    current_lengths + [stint_length]
                )
            )

        return results

    for stint_count in range(1, max_stints + 1):
        length_combinations = generate_lengths(
            race_laps,
            stint_count,
            []
        )

        for lengths in length_combinations:
            for compound_combination in product(
                compounds,
                repeat=stint_count
            ):
                strategies.append(
                    Strategy(
                        compounds=list(compound_combination),
                        stint_lengths=lengths
                    )
                )

    return strategies


def evaluate_strategy(
    strategy_name: str,
    strategy: Strategy,
    state: RaceState,
    lap_model: LapModel,
    fuel_consumption: float,
    pit_stop_time: float
) -> StrategyResult:
    simulation_state = replace(state)

    simulation_state.tyre_compound = strategy.compounds[0]

    stints = []

    for index, (compound, lap_count) in enumerate(
        zip(strategy.compounds, strategy.stint_lengths)
    ):
        stint = {
            "lap_count": lap_count
        }

        if index < len(strategy.compounds) - 1:
            stint["next_compound"] = strategy.compounds[index + 1]

        stints.append(stint)

    return simulate_strategy(
        strategy_name=strategy_name,
        state=simulation_state,
        lap_model=lap_model,
        stints=stints,
        fuel_consumption=fuel_consumption,
        pit_stop_time=pit_stop_time
    )