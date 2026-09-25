from domain.lap_model import LapModel
from domain.race_state import RaceState
from services.race_simulation_service import (
    advance_race_state,
    simulate_laps
)
from services.race_simulation_service import (
    advance_race_state,
    simulate_laps,
    calculate_stint_summary
)


def test_advance_race_state():
    state = RaceState(
        race_id=1,
        race_entry_id=1,
        current_lap=18,
        position=2,
        tyre_compound="Medium",
        tyre_age=0,
        fuel_load=50,
        status="Racing"
    )

    lap_model = LapModel(
        base_lap_time=90.0,
        tyre_degradation=0.08,
        fuel_penalty=0.03
    )

    next_state, lap_time = advance_race_state(
        state,
        lap_model,
        fuel_consumption=2
    )

    assert next_state.current_lap == 19
    assert next_state.tyre_age == 1
    assert lap_time == 91.58
    assert next_state.fuel_load == 48


def test_simulate_multiple_laps():
    state = RaceState(
        race_id=1,
        race_entry_id=1,
        current_lap=18,
        position=2,
        tyre_compound="Medium",
        tyre_age=0,
        fuel_load=50,
        status="Racing"
    )

    lap_model = LapModel(
        base_lap_time=90.0,
        tyre_degradation=0.08,
        fuel_penalty=0.03
    )

    lap_results = simulate_laps(
        state,
        lap_model,
        fuel_consumption=2,
        lap_count=3
    )

    assert len(lap_results) == 3

    assert lap_results[0].lap_number == 19
    assert lap_results[0].lap_time == 91.58
    assert lap_results[0].tyre_age == 1
    assert lap_results[0].fuel_load == 48
    assert lap_results[0].position == 2

    assert lap_results[2].lap_number == 21
    assert lap_results[2].tyre_age == 3
    assert lap_results[2].fuel_load == 44
    assert lap_results[2].position == 2

    assert state.current_lap == 21
    assert state.tyre_age == 3
    assert state.fuel_load == 44

def test_calculate_stint_summary():
    state = RaceState(
        race_id=1,
        race_entry_id=1,
        current_lap=18,
        position=2,
        tyre_compound="Medium",
        tyre_age=0,
        fuel_load=50,
        status="Racing"
    )

    lap_model = LapModel(
        base_lap_time=90.0,
        tyre_degradation=0.08,
        fuel_penalty=0.03
    )

    lap_results = simulate_laps(
        state,
        lap_model,
        fuel_consumption=2,
        lap_count=3
    )

    summary = calculate_stint_summary(lap_results)

    assert summary["lap_count"] == 3
    assert summary["total_time"] == 274.80
    assert summary["average_lap_time"] == 91.60
    assert summary["best_lap_time"] == 91.58
    assert summary["worst_lap_time"] == 91.62
    assert summary["fuel_remaining"] == 44
    assert summary["tyre_age"] == 3       