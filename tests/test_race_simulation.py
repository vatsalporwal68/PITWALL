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

    next_state = advance_race_state(state)

    assert next_state.current_lap == 19
    assert next_state.tyre_age == 1