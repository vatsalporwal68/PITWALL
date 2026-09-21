from dataclasses import dataclass


@dataclass
class LapModel:
    base_lap_time: float
    tyre_degradation: float

    def calculate_lap_time(self, tyre_age: int) -> float:
        return self.base_lap_time + (
            self.tyre_degradation * tyre_age
        )