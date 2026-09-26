from itertools import product

from domain.strategy import Strategy


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