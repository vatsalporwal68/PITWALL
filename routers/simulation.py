from fastapi import APIRouter

from domain.lap_model import LapModel
from domain.race_state import RaceState
from domain.strategy import Strategy

from schemas.simulation import (
    StrategyComparisonResponse,
    StrategySimulationRequest
)

from services.strategy_service import (
    evaluate_and_compare_strategies
)


router = APIRouter(
    prefix="/simulation",
    tags=["Simulation"]
)


@router.post(
    "/strategies",
    response_model=StrategyComparisonResponse
)
def simulate_strategies(
    request: StrategySimulationRequest
):
    state = RaceState(
        race_id=request.race_id,
        race_entry_id=request.race_entry_id,
        current_lap=0,
        position=request.position,
        tyre_compound="Unknown",
        tyre_age=0,
        fuel_load=request.fuel_load,
        status="Racing"
    )

    lap_model = LapModel(
        base_lap_time=request.base_lap_time,
        tyre_degradation=request.tyre_degradation,
        fuel_penalty=request.fuel_penalty,
        compound_performance=request.compound_performance
    )

    strategies = [
        Strategy(
            compounds=strategy.compounds,
            stint_lengths=strategy.stint_lengths
        )
        for strategy in request.strategies
    ]

    comparison = evaluate_and_compare_strategies(
        strategies=strategies,
        state=state,
        lap_model=lap_model,
        fuel_consumption=request.fuel_consumption,
        pit_stop_time=request.pit_stop_time
    )

    return comparison