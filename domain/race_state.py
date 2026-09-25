from dataclasses import dataclass


@dataclass
class RaceState:
    race_id: int
    race_entry_id: int
    current_lap: int
    position: int
    tyre_compound: str
    tyre_age: int
    fuel_load: float
    status: str

    def advance_lap(self):
        self.current_lap += 1
        self.tyre_age += 1


@dataclass
class LapResult:
    lap_number: int
    lap_time: float
    tyre_age: int
    fuel_load: float
    position: int