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
from services.race_simulation_service import (
    advance_race_state,
    simulate_laps,
    calculate_stint_summary,
    perform_pit_stop
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

def test_perform_pit_stop():
    state = RaceState(
        race_id=1,
        race_entry_id=1,
        current_lap=25,
        position=3,
        tyre_compound="Medium",
        tyre_age=18,
        fuel_load=30,
        status="Racing"
    )

    updated_state = perform_pit_stop(
        state,
        new_compound="Hard"
    )

    assert updated_state.tyre_compound == "Hard"
    assert updated_state.tyre_age == 0
    assert updated_state.current_lap == 25
    assert updated_state.position == 3

def test_multi_stint_simulation():
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

    first_stint = simulate_laps(
        state,
        lap_model,
        fuel_consumption=2,
        lap_count=3
    )

    assert first_stint[-1].lap_number == 21
    assert first_stint[-1].tyre_age == 3

    perform_pit_stop(
        state,
        new_compound="Hard"
    )

    assert state.tyre_compound == "Hard"
    assert state.tyre_age == 0

    second_stint = simulate_laps(
        state,
        lap_model,
        fuel_consumption=2,
        lap_count=2
    )

    assert second_stint[0].lap_number == 22
    assert second_stint[0].tyre_age == 1
    assert second_stint[1].lap_number == 23
    assert second_stint[1].tyre_age == 2               