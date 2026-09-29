from pydantic import BaseModel, Field, model_validator


class StrategyInput(BaseModel):
    compounds: list[str] = Field(min_length=1)
    stint_lengths: list[int] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_strategy(self):
        if len(self.compounds) != len(self.stint_lengths):
            raise ValueError(
                "Number of compounds must match number of stint lengths"
            )

        if any(length <= 0 for length in self.stint_lengths):
            raise ValueError(
                "Stint lengths must be greater than zero"
            )

        return self


class StrategySimulationRequest(BaseModel):
    race_id: int
    race_entry_id: int
    race_laps: int = Field(gt=0)

    position: int = Field(gt=0)
    fuel_load: float = Field(ge=0)

    fuel_consumption: float = Field(gt=0)
    pit_stop_time: float = Field(gt=0)

    base_lap_time: float = Field(gt=0)
    tyre_degradation: float = Field(ge=0)
    fuel_penalty: float = Field(ge=0)

    compound_performance: dict[str, float]

    strategies: list[StrategyInput] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_strategies(self):
        for strategy in self.strategies:
            if sum(strategy.stint_lengths) != self.race_laps:
                raise ValueError(
                    "Strategy stint lengths must equal race laps"
                )

        return self


class StrategyResultResponse(BaseModel):
    strategy_name: str
    total_race_time: float
    pit_stops: int


class StrategyComparisonResponse(BaseModel):
    strategies: list[StrategyResultResponse]
    fastest_strategy: str
    time_difference: dict[str, float]