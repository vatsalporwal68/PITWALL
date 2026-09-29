from fastapi import HTTPException

from domain.lap_model import LapModel
from domain.race_state import RaceState
from domain.strategy import Strategy
from models import Race as RaceModel
from services.strategy_service import evaluate_and_compare_strategies


def run_race_simulation(
    race_id: int,
    race_entry_id: int,
    db,
    strategies: list[Strategy],
    fuel_load: float,
    fuel_consumption: float,
    pit_stop_time: float,
    base_lap_time: float,
    tyre_degradation: float,
    fuel_penalty: float,
    compound_performance: dict[str, float]
):
    race = (
        db.query(RaceModel)
        .filter(RaceModel.id == race_id)
        .first()
    )

    if race is None:
        raise HTTPException(
            status_code=404,
            detail="Race not found"
        )

    race_entry = next(
        (
            entry
            for entry in race.race_entries
            if entry.id == race_entry_id
        ),
        None
    )

    if race_entry is None:
        raise HTTPException(
            status_code=404,
            detail="Race entry not found"
        )

    state = RaceState(
        race_id=race.id,
        race_entry_id=race_entry.id,
        current_lap=0,
        position=race_entry.grid_position,
        tyre_compound="Unknown",
        tyre_age=0,
        fuel_load=fuel_load,
        status=race_entry.status
    )

    lap_model = LapModel(
        base_lap_time=base_lap_time,
        tyre_degradation=tyre_degradation,
        fuel_penalty=fuel_penalty,
        compound_performance=compound_performance
    )

    return evaluate_and_compare_strategies(
        strategies=strategies,
        state=state,
        lap_model=lap_model,
        fuel_consumption=fuel_consumption,
        pit_stop_time=pit_stop_time
    )