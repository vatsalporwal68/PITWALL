from domain.race_state import RaceState
from services.race_state_service import get_race_state


def test_get_race_state(client):
    from database import SessionLocal

    db = SessionLocal()

    try:
        state = get_race_state(1, db)

        assert state is not None
        assert state.race_id == 1
        assert state.race_entry_id == 1
        assert state.position == 3
        assert state.status == "Racing"
        assert state.current_lap == 0
        assert state.tyre_compound == "Unknown"
        assert state.tyre_age == 0
        assert state.fuel_load == 0

    finally:
        db.close()


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

    state.advance_lap()

    assert state.current_lap == 19
    assert state.tyre_age == 1

def test_change_tyre():
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

    state.change_tyre("Hard")

    assert state.tyre_compound == "Hard"
    assert state.tyre_age == 0
    assert state.current_lap == 25
    assert state.position == 3    
        