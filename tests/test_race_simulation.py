from domain.lap_model import LapModel
from domain.race_state import RaceState
from services.race_simulation_service import advance_race_state


def test_advance_race_state():
    state = RaceState(
        race_id=1,
        race_entry_id=1,
        current_lap=18,
        position=2,
        tyre_compound="Medium",
        tyre_age=0,
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
        fuel_load=50
    )

    assert next_state.current_lap == 19
    assert next_state.tyre_age == 1
    assert lap_time == 91.58