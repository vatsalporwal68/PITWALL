from dataclasses import dataclass


@dataclass
class RaceState:
    race_id: int
    race_entry_id: int
    current_lap: int
    position: int
    tyre_compound: str
    tyre_age: int
    status: str

    def advance_lap(self):
        self.current_lap += 1
        self.tyre_age += 1