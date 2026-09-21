from domain.race_state import RaceState
from models import RaceEntry as RaceEntryModel


def get_race_state(race_entry_id: int, db):
    race_entry = (
        db.query(RaceEntryModel)
        .filter(RaceEntryModel.id == race_entry_id)
        .first()
    )

    if race_entry is None:
        return None

    return RaceState(
        race_id=race_entry.race_id,
        race_entry_id=race_entry.id,
        current_lap=0,
        position=race_entry.grid_position,
        tyre_compound="Unknown",
        tyre_age=0,
        status=race_entry.status
    )