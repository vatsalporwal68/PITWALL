from fastapi import APIRouter, Depends

from database import get_db
from domain.strategy import Strategy

from schemas.simulation import (
    StrategyComparisonResponse,
    StrategySimulationRequest
)

from services.simulation_service import run_race_simulation


router = APIRouter(
    prefix="/simulation",
    tags=["Simulation"]
)


@router.post(
    "/strategies",
    response_model=StrategyComparisonResponse
)
def simulate_strategies(
    request: StrategySimulationRequest,
    db=Depends(get_db)
):
    strategies = [
        Strategy(
            compounds=strategy.compounds,
            stint_lengths=strategy.stint_lengths
        )
        for strategy in request.strategies
    ]

    comparison = run_race_simulation(
        race_id=request.race_id,
        race_entry_id=request.race_entry_id,
        db=db,
        strategies=strategies,
        fuel_load=request.fuel_load,
        fuel_consumption=request.fuel_consumption,
        pit_stop_time=request.pit_stop_time,
        base_lap_time=request.base_lap_time,
        tyre_degradation=request.tyre_degradation,
        fuel_penalty=request.fuel_penalty,
        compound_performance=request.compound_performance
    )

    return comparison