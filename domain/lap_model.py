from dataclasses import dataclass


@dataclass
class LapModel:
    base_lap_time: float
    tyre_degradation: float
    fuel_penalty: float
    compound_performance: dict[str, float]

    def calculate_lap_time(
        self,
        tyre_age: int,
        fuel_load: float,
        tyre_compound: str
    ) -> float:
        tyre_effect = self.tyre_degradation * tyre_age
        fuel_effect = self.fuel_penalty * fuel_load

        compound_effect = self.compound_performance.get(
            tyre_compound,
            0.0
        )

        return (
            self.base_lap_time
            + tyre_effect
            + fuel_effect
            + compound_effect
        )