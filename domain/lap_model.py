from dataclasses import dataclass


@dataclass
class LapModel:
    base_lap_time: float
    tyre_degradation: float
    fuel_penalty: float

    def calculate_lap_time(
        self,
        tyre_age: int,
        fuel_load: float
    ) -> float:
        tyre_effect = self.tyre_degradation * tyre_age
        fuel_effect = self.fuel_penalty * fuel_load

        return (
            self.base_lap_time
            + tyre_effect
            + fuel_effect
        )