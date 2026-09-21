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

    finally:
        db.close()
        