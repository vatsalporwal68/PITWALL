from dataclasses import dataclass


@dataclass
class Strategy:
    compounds: list[str]
    stint_lengths: list[int]

    @property
    def stint_count(self) -> int:
        return len(self.compounds)

    @property
    def total_laps(self) -> int:
        return sum(self.stint_lengths)